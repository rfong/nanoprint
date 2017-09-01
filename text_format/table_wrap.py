"""Utils for text wrapping tables"""

from string_utils import rep_str, pad_str, right_index_of


def break_to_width(s, width, hyphen_break=False):
  """Break a string `s` into a list of strings all not exceeding `width`"""
  if width == 1:
    return list(s)
  output = []
  while len(s) > 0:
    # Remainder is short enough
    if len(s) <= width:
      output.append(s)
      return output
    # Try to break on space
    try:
      ind = right_index_of(s, ' ', width)
      output.append(s[:ind])
      s = s[ind+1:]
    # If not possible, force break line
    except ValueError:
      if hyphen_break:
        ind = width - 1
        output.append(s[:ind] + ('-' if width > 1 else ''))
        s = s[ind:]
      else:
        output.append(s[:width])
        s = s[width:]
    s = s.strip()
  return output

def wrap(s, width, hyphen_break=False):
  """
  Break a string `s` into a list of strings all not exceeding `width`, and
  pad each to `width`
  """
  assert type(s) == str
  return [pad_str(substr, width) for substr in
          break_to_width(s, width, hyphen_break=hyphen_break)]

def zip_longest_strings(arr):
  """
  Transposes a 2D array of strings. Similar to Python3.x's
  itertools.zip_longest except that default value gets padded to blank string
  """
  # Pad lengths with whitespace strings
  max_row_len = max(len(row) for row in arr)
  arr = [row + [rep_str(' ', len(row[0]))] * (max_row_len - len(row))
         for row in arr]
  # Transpose
  return map(list, zip(*arr))

def wrap_row(row, col_widths, hyphen_break=False, field_sep=' | '):
  """
  Break fields in row and pad so they conform to column widths.
  Return single string representing the row with line breaks inserted.
  """
  assert len(row) == len(col_widths)
  # Broken fields (padded)
  broken_fields = [
    wrap(field, width, hyphen_break=hyphen_break)
    for field, width in zip(row, col_widths)
  ]
  # Transpose & join each broken line
  return '\n'.join(
    field_sep.join(line) for line in zip_longest_strings(broken_fields)
  )
