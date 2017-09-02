"""
Nanoprinter gui

Note: to use standalone screen with OLED bonnet buttons:
plug VCC, GND, SCL, SDA into bonnet
plug button pins
"""

from collections import OrderedDict
import socket
import time

import RPi.GPIO as GPIO

import core as nanoprint_core
from core import PINS
from menu import Menu


def main():
  display = nanoprint_core.get_display()

  options = OrderedDict()
  options['the cutest menu'] = ['A', 'B', 'C']
  options['network printer'] = ['print me!', 'print you!']
  options['documents'] = ['tap drill US', 'tap drill metric', 'OLL', 'OLL_forgot']
  options['notepad'] = None
  options['fortune teller'] = []
  options['arcane bytes'] = None
  options['necronomicon'] = None
  options['bad stenography'] = None

  menu = Menu(display, options)


if __name__ == '__main__':
  main()
