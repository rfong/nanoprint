from collections import namedtuple


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
