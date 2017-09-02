from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

import RPi.GPIO as GPIO

from core import PINS


class BaseInterface(object):

  REFRESH_TIME = 0.01

  def __init__(self, display):
    """
    :param display: a reference to an initialized SSD1306_128_64 object
    """
    self.display = display
    display.begin()
    display.clear()
    display.display()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = display.width
    height = display.height
    self.image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    self.draw = ImageDraw.Draw(self.image)
    self.font = ImageFont.load_default()

    self.clear()

    try:
      while 1:
        self.loop()
        self.update_display()
    except KeyboardInterrupt: 
      GPIO.cleanup()

  def loop(self):
    """Extend me"""
    raise NotImplementedError()

  def clear(self):
    # Draw a black filled box to clear the image.
    self.draw.rectangle((0,0,self.display.width,self.display.height), outline=0, fill=0)

  def update_display(self):
    self.display.image(self.image)
    self.display.display()
    time.sleep(self.REFRESH_TIME)
    self.clear()

  def is_button_released(self, name):
    """:name: should correspond to a key in core.PINS"""
    assert name in PINS, "%s is not in core.PINS" % name
    return GPIO.input(PINS[name])

  def is_button_pressed(self, name):
    """:name: should correspond to a key in core.PINS"""
    return not self.is_button_released(name)
