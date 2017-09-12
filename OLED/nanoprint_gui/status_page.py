"""
Status page. Similar to menu, but continuously polls functions to display
info and is not very interactive (can only go back)
"""


from collections import OrderedDict
import socket

from menu import Menu
from shims import Shim


class StatusPage(Menu):

  def __init__(self, disp, polls, has_parent=True):
    """
    :disp: an instance of an Adafruit_SSD1306 display
    :polls: an OrderedDict where:
      keys: attribute names (strings)
      values: functions that return attr values, independent of menu state
        (may also be None)
    :has_parent: was this instantiated by a parent menu?
    """
    self.polls = polls
    super(StatusPage, self).__init__(disp, [], has_parent=has_parent)

  def poll(self, attr):
    """Get value from a specific poll"""
    assert attr in self.polls
    if self.polls[attr] is None:
      return None
    return self.polls[attr]()

  def update_options(self):
    """Poll & update options"""
    # Evaluate once
    self.updates = {key: self.poll(key) for key in self.polls.keys()}
    # Update text for display
    self.options = [
      '%s' if self.updates[key] is None
      else '%s: %s' % (key, self.updates[key])
      for key in self.polls.keys()
    ]

  def loop(self):
    self.update_options()
    return super(StatusPage, self).loop()


def get_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  ip_addr = s.getsockname()[0]
  s.close()
  return ip_addr

network_status_options = OrderedDict()
network_status_options['IP'] = get_ip

def run_network_status_page_factory(display):
  def run_network_status_page():
    StatusPage(display, network_status_options)
  return run_network_status_page

def NetworkStatusShimFactory(display):
  return Shim(run_network_status_page_factory(display), None, None)
