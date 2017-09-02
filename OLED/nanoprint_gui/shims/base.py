from collections import namedtuple
import os


Shim = namedtuple('Shim', [

  'run',
  # type: function
  # Run the shim

  'loading_message',
  # type: str
  # Optional loading message to display while shim is running

  'finished_message'
  # type: str
  # Optional message to display after shim finishes

], verbose=True)


DOCS_BASE_PATH = '/home/rfong/text_format/docs'

def get_doc_path(rel_path):
  return os.path.join(DOCS_BASE_PATH, rel_path)

BREAKPATH = get_doc_path('linebreaks.txt')
