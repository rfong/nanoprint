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

  selected = 0

  def __init__(self, disp, options):
    self.options = options
    super(NanoprintMenu, self).__init__(disp)

  def loop(self):
    #ip_addr = get_ip()
    #if ip_addr:
    #  self.write_line("IP: " + ip_addr)
    #else:
    #  self.write_line("Searching for Wi-Fi...")
    #self.write_line("hihihihi", line=1)

    self.draw_legend()

    # Draw menu
    for i, opt in enumerate(self.options):
      self.write_line(opt, line=i)
    self.draw_line_pointer(self.selected)

    # Handle button presses & draw status
    if self.is_button_pressed('A'):
      self.scroll()

  def draw_legend(self):
    """Draw button legend & status"""
    legend_width = 14
    legend_x = self.display.width - legend_width - 1
    legend_center = legend_x + legend_width/2

    # Mark out button legend
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
    # Button C - back arrow
    self.draw.polygon(
      translate_coords(
        [(0,3), (6,0), (6,6)],
        legend_center - 3, self.display.height - 6 - self.PADDING
      ),
      outline=255,
      fill=int(self.is_button_pressed('A'))
    )

  # Internal state helpers

  def scroll(self):
    self.selected = (self.selected + 1) % len(self.options)

  # Constants

  LINE_HEIGHT = 10
  PADDING = 5

  BASE_COORDS = AttrDict({
  })

  # Drawing helpers

  def write_line(self, text, line=0):
    """Write text on line (check width; will overflow)"""
    self.draw.text(
      (2 * self.PADDING, self.PADDING + line * self.LINE_HEIGHT),
      text, font=self.font, fill=1)

  def draw_line_pointer(self, line, fill=0):
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
