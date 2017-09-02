from collections import OrderedDict
import socket

from base_interface import BaseInterface
from util import AttrDict, Vector2D


def get_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  ip_addr = s.getsockname()[0]
  s.close()
  return ip_addr

def translate_coords(coords, x, y):
  """coords should be a list of 2D tuples"""
  return [(c[0] + x, c[1] + y) for c in coords]


class NanoprintMenu(BaseInterface):

  def __init__(self, disp, nested_options):
    """
    :disp: an instance of a Adafruit_SSD1306 display
    :nested_options: either an OrderedDict or a list at each level
    """
    assert (type(nested_options) == list or
            isinstance(nested_options, OrderedDict)), (
            "must pass list or OrderedDict of options")
    if type(nested_options) == list:
      self.options = nested_options
      self.nested_options = None
    else:
      self.options = nested_options.keys()  # top level options
      self.nested_options = nested_options

    super(NanoprintMenu, self).__init__(disp)

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
      self.write_line(opt, line=i)
    self.draw_line_pointer(self.current_index)

    # Handle button presses
    if self.is_button_pressed('A'):
      self.increment_select()
    if self.is_button_first_pressed('B'):
      self.selected_action()

    for name in self.button_names:
      self.was_button_pressed[name] = self.is_button_pressed(name)

  def draw_legend(self):
    """Draw button legend & status"""
    legend_width = 14
    legend_x = self.display.width - legend_width - 1
    legend_center = legend_x + legend_width/2

    # Mark out button legend bounds
    self.draw_vertical_line(legend_x, fill=1)
    self.draw_vertical_line(self.display.width-1, fill=1)

    # Button A - down arrow
    self.draw.polygon(
      translate_coords([(0,0), (6,0), (3, 6)], legend_center - 3, self.PADDING),
      outline=255,
      fill=int(self.is_button_pressed('A'))
    )
    # Button B - circle
    self.draw_circle(
      legend_center, self.display.height / 2, 6,
      outline=255,
      fill=int(self.is_button_pressed('B'))
    )
    # Button C - back arrow  (not implemented in hardware yet)
    self.draw.polygon(
      translate_coords(
        [(0,3), (6,0), (6,6)],
        legend_center - 3, self.display.height - 6 - self.PADDING
      ),
      outline=255,
      fill=int(self.is_button_pressed('A'))
    )

  # Internal state management

  current_index = 0  # Current selection index
  scroll_frame = 0  # Top index of scroll frame
  button_names = ['A', 'B']

  was_button_pressed = {name: False for name in button_names}  # on prev loop
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
    children = self.nested_options.values()[self.current_index]
    if not children:
      return
    # Create new menu from node children
    submenu = NanoprintMenu(self.display, children)

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

  BASE_COORDS = AttrDict({
  })

  # Drawing helpers

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
