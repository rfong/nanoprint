""" Interactive/scrollable configurable menu functionality """


from collections import OrderedDict
import socket
import time

import RPi.GPIO as GPIO

from base_interface import BaseInterface
from shims import Shim
from util import AttrDict


def get_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  ip_addr = s.getsockname()[0]
  s.close()
  return ip_addr

def translate_coords(coords, x, y):
  """coords should be a list of 2D tuples"""
  return [(c[0] + x, c[1] + y) for c in coords]


class Menu(BaseInterface):

  def __init__(self, disp, nested_options, has_parent=False):
    """
    :disp: an instance of a Adafruit_SSD1306 display
    :nested_options: top level must be:
      - an OrderedDict (specifies a nested option list)
      - a list (specifies plain text options)
      child levels may also be None or Shim
      # Note: currently this enforces uniqueness -- may want to change that
      # in the future
    :has_parent: was this instantiated by a parent menu?
    """
    self.has_parent = has_parent
    if type(nested_options) == list:
      self.options = nested_options
      self.nested_options = None
    elif isinstance(nested_options, OrderedDict):
      self.options = nested_options.keys()  # top level options
      self.nested_options = nested_options
    else:
      raise Exception("Options passed must be OrderedDict or list")

    print('Show menu:', self.options)

    super(Menu, self).__init__(disp)

  def loop(self):
    """ Main render loop """
    #ip_addr = get_ip()
    #if ip_addr:
    #  self.write_line("IP: " + ip_addr)
    #else:
    #  self.write_line("Searching for Wi-Fi...")
    #self.write_line("hihihihi", line=1)

    #self.draw_legend()

    # Draw menu
    for i, opt in enumerate(self.options):
      if self.is_line_entirely_in_display(i):
        self.write_line(opt, line=i)
    self.draw_line_pointer(self.current_index)

    # Handle button presses
    if self.is_button_pressed(self.gpio.NEXT):
      self.increment_select()
    if self.is_button_first_pressed(self.gpio.SELECT):
      self.selected_action()
    if self.is_button_first_pressed(self.gpio.BACK) and self.has_parent:
      return True  # quits outer render loop

    for name in self.gpio.values():
      self.was_button_pressed[name] = self.is_button_pressed(name)

  def draw_legend(self):
    """Draw button legend & status"""
    legend_width = 6
    legend_x = self.display.width - legend_width - 1
    legend_center = legend_x + legend_width/2

    # Button A - down arrow
    self.draw.polygon(
      translate_coords([(0,0), (6,0), (3, 6)], legend_center - 3, self.PADDING),
      outline=255,
      fill=int(self.is_button_pressed(self.gpio.NEXT))
    )
    # Button B - circle
    self.draw_circle(
      legend_center, self.display.height / 2, 6,
      outline=255,
      fill=int(self.is_button_pressed(self.gpio.SELECT))
    )
    # Button C - back arrow
    self.draw.polygon(
      translate_coords(
        [(0,3), (6,0), (6,6)],
        legend_center - 3, self.display.height - 6 - self.PADDING
      ),
      outline=255,
      fill=int(self.is_button_pressed(self.gpio.BACK))
    )

  # Internal state management

  current_index = 0  # Current selection index
  scroll_frame = 0  # Top index of scroll frame

  # Mapping from gpio functions to pins
  gpio = AttrDict({
    'NEXT': 'A',
    'SELECT': 'B',
    'BACK': 'C',
  })

  # Was button pressed on prev loop?
  was_button_pressed = {name: False for name in gpio.values()}

  def is_button_first_pressed(self, name):
    """Clean button press detection. Ignores continuous pressing."""
    return self.is_button_pressed(name) and not self.was_button_pressed[name]

  def increment_select(self):
    self.current_index = (self.current_index + 1) % len(self.options)
    if not self.is_line_entirely_in_display(self.current_index):
      self.scroll_frame += 1
    if self.current_index == 0:
      self.scroll_frame = 0

  def selected_action(self):
    """Perform action for currently selected item"""
    if not self.nested_options:  # Flat list
      return
    child = self.nested_options.values()[self.current_index]

    # No children, do nothing
    if not child:
      return

    # Child is a Shim, perform action
    elif isinstance(child, Shim):
      if child.loading_message:
        self.show_loading_screen(child.loading_message)
      child.run()
      if child.finished_message:
        time.sleep(0.3)
        self.show_loading_screen(child.finished_message)
        time.sleep(0.3)

    # Nested children, open a submenu
    else:
      submenu = Menu(self.display, child, has_parent=True)

    # TODO: add 3rd button and then implement back functionality

  # Line convenience helpers

  def get_display_line_index(self, line):
    """Translate line index to the scroll frame"""
    return line - self.scroll_frame

  def is_line_entirely_in_display(self, line):
    return (
      (self.get_menu_line_y(line + 1) < self.display.height) and
      (self.get_menu_line_y(line) >= 0))

  def is_line_out_of_frame(self, line):
    return (
      (self.get_menu_line_y(line + 1) < 0) or
      (self.get_menu_line_y(line) >= self.display.height)
    )

  # Constants

  LINE_HEIGHT = 10
  PADDING = 5

  # Drawing helpers

  def show_loading_screen(self, text):
    """Redraw screen with a loading message"""
    self.clear()
    # TODO: wrap text
    self.write_line(text, line=1)
    self.update_display()

  def get_menu_line_y(self, line):
    """:line: index is in absolute frame, not display frame"""
    return self.PADDING + self.get_display_line_index(line) * self.LINE_HEIGHT

  def write_line(self, text, line=0):
    """Write text on line (check width; will overflow)"""
    self.draw.text(
      (2 * self.PADDING, self.get_menu_line_y(line)),
      text, font=self.font, fill=1)

  def draw_line_pointer(self, line, fill=0):
    line = self.get_display_line_index(line)
    self.draw.polygon(
      translate_coords([(2,8), (6,10.5), (2,13)], 0, line * self.LINE_HEIGHT),
      outline=255, fill=fill)

  def draw_vertical_line(self, x, y0=0, y1=None, **kwargs):
    if y1 is None:
      y1 = self.display.height
    self.draw.line([(x, y0), (x, y1)], **kwargs)

  def draw_horizontal_line(self, y, x0=0, x1=None, **kwargs):
    if x1 is None:
      x1 = self.display.width
    self.draw.line([(x0, y), (x1, y)], **kwargs)

  def draw_circle(self, x, y, d, **kwargs):
    """Draw circle centered at (x, y) with diameter d"""
    r = d * 0.5
    self.draw.ellipse((x-r, y-r, x+r, y+r), **kwargs)
