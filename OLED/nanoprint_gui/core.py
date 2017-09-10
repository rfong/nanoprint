""" Hardware setup """


import Adafruit_SSD1306
import RPi.GPIO as GPIO


# Name to pin number mapping
PINS = {
  #'A': 5,
  #'B': 6,
  'RST': 24,
  'A': 27,  # green pushbutton
  'B': 22,  # blue pushbutton
  'C': 23,  # purple pushbutton
  'TX_SWITCH': 25,  # Transistor switch control
  'PIEZO': 18,  # piezo out
}

_display = None

def setup_hardware():
  """Hardware init."""
  global _display

  # OLED setup
  GPIO.setmode(GPIO.BCM) 
  _display = Adafruit_SSD1306.SSD1306_128_64(rst=PINS['RST'], i2c_address=0x3C)

  # Pushbutton pins
  GPIO.setup(PINS['A'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(PINS['B'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(PINS['C'], GPIO.IN, pull_up_down=GPIO.PUD_UP)

  # Printer data line switch.
  # Set high as soon as menu is ready, don't need to change again.
  # Prevents garbage printing from UART low glitch on Raspberry Pi boot.
  GPIO.setup(PINS['TX_SWITCH'], GPIO.OUT, initial=GPIO.HIGH)

  # Piezo (how to PWM?)
  GPIO.setup(PINS['PIEZO'], GPIO.OUT, initial=GPIO.LOW)


def set_GPIO_output(name, state):
  assert name in PINS
  GPIO.output(PINS[name], state)


def get_display():
  if not _display:
    setup_hardware()
  return _display
