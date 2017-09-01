"""Common string utils for tinyprinting"""

def rep_str(cha, length):
  """Return string that is `cha` repeated `length` times"""
  return ''.join([cha] * length)

def pad_str(s, length):
  """Pad a string with whitespace to len `length`"""
  assert length >= 0
  assert len(s) <= length, '"%s" is wider than %d chars' % (s, length)
  return s + rep_str(' ', length - len(s))

def right_index_of(s, c, k):
  """Returns index of first `c` that is <= `k`"""
  return k - s[:k+1][::-1].index(c)  # Reverse, index, unreverse
