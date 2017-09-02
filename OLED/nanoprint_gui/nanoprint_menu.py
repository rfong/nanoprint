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

    for i, opt in enumerate(self.options):
      self.write_line(opt, line=i)
    self.draw_line_pointer(self.selected)

    if self.is_button_pressed('A'):
      self.draw.ellipse((70,40,90,60), outline=255, fill=1) #A button filled
      self.scroll()
    else:
      self.draw.ellipse((70,40,90,60), outline=255, fill=0) #A button
    if self.is_button_pressed('B'):
      self.draw.ellipse((100,20,120,40), outline=255, fill=1) #B button filled
    else:
      self.draw.ellipse((100,20,120,40), outline=255, fill=0) #B button

  # Internal state helpers

  def scroll(self):
    self.selected = (self.selected + 1) % len(self.options)

  # Constants

  LINE_HEIGHT = 10

  BASE_COORDS = AttrDict({
    'LINE_POINTER': [(2,8), (6,10), (2,13)],
  })

  # Drawing helpers

  def write_line(self, text, line=0):
    """Write text on line (check width; will overflow)"""
    self.draw.text(
      (10, 5 + line * self.LINE_HEIGHT), text, font=self.font, fill=1)

  def draw_line_pointer(self, line):
    self.draw.polygon(
      translate_coords(self.BASE_COORDS.LINE_POINTER,
                       0, line * self.LINE_HEIGHT),
      outline=255, fill=0)  #Up
    # right pointing triangle: 60,60 42,21 42,41
