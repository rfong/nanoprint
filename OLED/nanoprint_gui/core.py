""" Hardware setup """


import Adafruit_SSD1306
import RPi.GPIO as GPIO


PINS = {
  'A': 5,
  'B': 6,
  'RST': 24,
}

_display = None

def setup_hardware():
  """Hardware init."""
  global _display

  # OLED setup
  GPIO.setmode(GPIO.BCM) 
  _display = Adafruit_SSD1306.SSD1306_128_64(rst=PINS['RST'], i2c_address=0x3C)

  # Pushbutton pins
  GPIO.setup(PINS['A'], GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
  GPIO.setup(PINS['B'], GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up


def get_display():
  if not _display:
    setup_hardware()
  return _display
