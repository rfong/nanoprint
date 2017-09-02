"""
Display my IP on an OLED SSD1306 screen
"""

import socket
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import Adafruit_SSD1306
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM) 
RST = 24
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)


def get_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  ip_addr = s.getsockname()[0]
  s.close()
  return ip_addr

def main():
  disp.begin()
  disp.clear()
  disp.display()

  # Create blank image for drawing.
  # Make sure to create image with mode '1' for 1-bit color.
  width = disp.width
  height = disp.height
  image = Image.new('1', (width, height))

  # Get drawing object to draw on image.
  draw = ImageDraw.Draw(image)
  font = ImageFont.load_default()

  # Draw a black filled box to clear the image.
  draw.rectangle((0,0,width,height), outline=0, fill=0)

  def draw_text(text, line=0):
    draw.text((5, 5 + line * 10), text, font=font, fill=1)

  try:
    while 1:
      ip_addr = get_ip()
      if ip_addr:
        draw_text("IP: " + ip_addr)
      else:
        draw_text("Searching for Wi-Fi...")
      draw_text("hihihihi", line=1)

      disp.image(image)
      disp.display()   
      time.sleep(.01) 

  except KeyboardInterrupt: 
    GPIO.cleanup()


if __name__ == '__main__':
  main()
