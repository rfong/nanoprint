import os
import subprocess

from base import Shim, get_doc_path, BREAKPATH


def print_document_factory(abs_path, test=False):
  path = get_doc_path(abs_path)

  def print_document():
    bash_expr = (
      "head -n7 %s | cat - %s" % (path, BREAKPATH)
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
