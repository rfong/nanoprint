"""
Nanoprinter gui

Note: to use standalone screen with OLED bonnet buttons:
plug VCC, GND, SCL, SDA into bonnet
plug button pins
"""

import socket
import time

import RPi.GPIO as GPIO

import core as nanoprint_core
from core import PINS
from nanoprint_menu import NanoprintMenu


def main():
  display = nanoprint_core.get_display()
  menu = NanoprintMenu(display, ['Network printer', 'Documents', 'Notepad'])


if __name__ == '__main__':
  main()
