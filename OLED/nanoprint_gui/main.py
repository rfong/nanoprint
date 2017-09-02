"""
Nanoprinter gui

Note: to use standalone screen with OLED bonnet buttons:
plug VCC, GND, SCL, SDA into bonnet
plug button pins
"""

from collections import OrderedDict
import os
import socket
import time

import RPi.GPIO as GPIO

import core as nanoprint_core
from core import PINS
from menu import Menu

from shims import DocumentShimFactory, FortuneTellerShim


def main():
  display = nanoprint_core.get_display()

  options = OrderedDict()

  options['the cutest menu'] = ['A', 'B', 'C']
  options['network printer'] = ['print me!', 'print you!']

  docs = OrderedDict()
  docs['US drill clearance'] = DocumentShimFactory('drill_clearance_us.txt', test=True)
  docs['metric drill clearance'] = DocumentShimFactory('drill_clearance_metric.txt', test=True)
  docs['PLL (forgotten)'] = DocumentShimFactory('rubiks_PLL_forgot.txt', test=True)
  options['documents'] = docs

  options['notepad'] = None
  options['fortune teller'] = FortuneTellerShim
  options['arcane bytes'] = None
  options['necronomicon'] = None
  options['bad stenography'] = None

  menu = Menu(display, options)


if __name__ == '__main__':
  main()
