"""Utils for text wrapping tables"""

from string_utils import rep_str, pad_str, right_index_of


def find_break_acceptable_index(s, break_chrs, width):
  s = s[:width]
  for i in reversed(xrange(len(s))):
    if s[i] in break_chrs:
      return i
  return None


def break_to_width(s, width, hyphen_break=False, break_chrs=''):
  """Break a string `s` into a list of strings all not exceeding `width`"""
  if width == 1:
    return list(s)
  output = []
  while len(s) > 0:

    # Remainder is short enough
    if len(s) <= width:
      output.append(s)
      return output

    # Try to line break in an acceptable place
    space_ind = right_index_of(s, ' ', width)
    break_ind = find_break_acceptable_index(s, break_chrs, width)

    # If not possible, force break line
    if space_ind is None and break_ind is None:
      if hyphen_break:
        ind = width - 1
        output.append(s[:ind] + ('-' if width > 1 else ''))
        s = s[ind:]
      else:
        output.append(s[:width])
        s = s[width:]

    else:
      # If a nonspace char was found, we want to break *after* it
      if break_ind is not None:
        break_ind += 1

      # Break on the later point
      if break_ind is None or space_ind > break_ind:
        output.append(s[:space_ind])
        s = s[space_ind+1:]  # Skip over break spaces
      else:
        output.append(s[:break_ind])
        s = s[break_ind:]

    s = s.strip()
  return output


def wrap(s, width, hyphen_break=False, break_chrs=''):
  """
  Break a string `s` into a list of strings all not exceeding `width`, and
  pad each to `width`
  """
  assert type(s) == str
  return [pad_str(substr, width) for substr in
          break_to_width(s, width, hyphen_break=hyphen_break,
                         break_chrs=break_chrs)]


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


def wrap_row(row, col_widths, hyphen_break=False, field_sep=' | ',
             break_chrs=''):
  """
  Break fields in row and pad so they conform to column widths.
  Return single string representing the row with line breaks inserted.
  """
  assert len(row) == len(col_widths)
  # Broken fields (padded)
  broken_fields = [
    wrap(field, width, hyphen_break=hyphen_break, break_chrs=break_chrs)
    for field, width in zip(row, col_widths)
  ]
  # Transpose & join each broken line
  return '\n'.join(
    field_sep.join(line) for line in zip_longest_strings(broken_fields)
  )
