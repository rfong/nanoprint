import os
import random
import subprocess
import tempfile

from base import Shim, BREAKPATH


fortunes = [
  "you will have a good day :D",
  "you will hug a tiny printer",

  #"'single quote test'",
  #'double quote test "',
  #'horrible "quote \'nightmare test\'"',
]

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


FortuneTellerShim = Shim(print_random_fortune, None, None)
