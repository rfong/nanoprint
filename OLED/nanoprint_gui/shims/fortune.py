""" Shim for printing random fortunes """
# TODO: import auto text wrapping

import os
import random
import subprocess
import tempfile

from base import Shim, BREAKPATH


def print_random_fortune_factory(fortunes):
  def print_random_fortune():
    # Use a tempfile because using file I/O instead of strings in memory
    # solves character escape problems in the subprocess bash expression
    tmpfile = tempfile.NamedTemporaryFile(delete=False)
    try:
      tmpfile.write(random.choice(fortunes))
      tmpfile.file.read()  # why does this fix it???
      # add extra linebreaks -- hard to tear off paper if it's too short
      bash_expr = 'cat %s %s %s' % (tmpfile.name, BREAKPATH, BREAKPATH)
      proc = subprocess.Popen((
        'sudo stty -F /dev/serial0 9600 && ' +
        'sudo sh -c "%s > /dev/serial0"' % bash_expr
      ), shell=True)
      proc.wait()
    finally:
      os.remove(tmpfile.name)
  return print_random_fortune


CuteFortuneShim = Shim(print_random_fortune_factory([
  "you will have a good day C:",
  "you will hug a tiny printer ;)",
]), None, None)


SassyFortuneShim = Shim(print_random_fortune_factory([
  'Today you will find a food you crave.',
  'We were born naked, we will die naked, and there might be some nudity in between.',
  'People envy your hair. Let them.',
  'You will be sassed tonight.',
  'You have a dog.',
  'No good can come of eating Go stones.',
  "It's never too late to start your Rumspringa.",
  "By Grabthar's hammer...YOU SHALL BE AVENGED",
  'You will not get scurvy. Tonight.',
]), None, None)


string_tests = [
  "'single quote test'",
  'double quote test "',
  'horrible "quote \'nightmare test\'"',
]
