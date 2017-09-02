import os
import subprocess

from base import Shim


DOCS_BASE_PATH = '/home/rfong/text_format/docs'

def print_document_factory(abs_path, test=False):
  path = os.path.join(DOCS_BASE_PATH, abs_path)
  breakpath = os.path.join(DOCS_BASE_PATH, 'linebreaks.txt')

  def print_document():
    bash_expr = (
      "head -n7 %s | cat - %s" % (path, breakpath)
      if test
      else "cat %s %s" % (path, breakpath)
    )
    subprocess.call((
      'sudo stty -F /dev/serial0 9600 && ' +
      # double quotes important in the sudo sh expr here (weird bash reasons)
      'sudo sh -c "%s > /dev/serial0"' % bash_expr
    ), shell=True)
  return print_document


def DocumentShimFactory(abs_path, test=False):
  return Shim(
    print_document_factory(abs_path, test=test),
    'Printing...',
    'Done!'
  )
