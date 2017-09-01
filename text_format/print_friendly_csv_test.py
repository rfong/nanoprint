"""Unit tests for CSV/text formatting functionality"""

import unittest


class TestCase(unittest.TestCase):
  """Base class for test helpers"""

  def run_function_on_case(self, test_function, expected, args=None,
                           kwargs=None):
    """
    Run a function and evaluate against expected output, with nice
    error messages.
    """
    # Manually set defaults to avoid weird Python kwarg scoping issue
    if args is None:
      args = []
    if kwargs is None:
      kwargs = {}
    # Run test function
    result = test_function(*args, **kwargs)
    self.assertEqual(result, expected, ' '.join([
      '%s(*%s, **%s)' % (test_function.__name__,
                         args.__repr__(),
                         kwargs.__repr__()),
      'yielded', result.__repr__(),
      'expected', expected.__repr__()
    ]))


from string_utils import rep_str, pad_str, right_index_of

class TestStringUtils(TestCase):

  def test_rep_str(self):
    self.assertEqual(rep_str('a', 5), 'aaaaa')
    self.assertEqual(rep_str('ab', 3), 'ababab')

  def test_pad_str(self):
    self.assertEqual(pad_str('a', 4), 'a   ')
    self.assertEqual(pad_str('abab', 5), 'abab ')
    with self.assertRaises(Exception):
      pad_str('abababa', 2)
    with self.assertRaises(Exception):
      pad_str('', -1)

  def test_right_index_of(self):
    self.assertEqual(right_index_of('foo bar', ' ', 4), 3)
    self.assertEqual(right_index_of('foo bar', ' ', 3), 3)
    self.assertEqual(right_index_of('foo bar', ' ', 2), None)


from table_wrap import find_break_acceptable_index, break_to_width, wrap_row

class TestTableWrap(TestCase):

  def test_find_break_acceptable_index(self):
    cases = [
      (('boop', '-', 3), None),
      (('blop-blop', '-', 5), 4),
      (('blop-blop', '-', 4), None),
      (('pew-!', '-', 5), 3),
      (('pew-!', '-!', 5), 4),
      (('pew!-', '-!', 5), 4),
      (('abcd-efghi', '-', 5), 4),
    ]
    for args, expected in cases:
      self.run_function_on_case(
        find_break_acceptable_index, expected, args=args)

  def test_break_to_width(self):
    # <args>, <expected output>
    common_cases = [
      (('foo', 1), ['f', 'o', 'o']),  # width=1 ignores hyphen break
      (('foo bar', 3), ['foo', 'bar']),
      (('foo bar ', 3), ['foo', 'bar']),
      (('lorem ipsum dolor sit', 11), ['lorem ipsum', 'dolor sit']),
      (('lorem ipsum dolor sit', 8), ['lorem', 'ipsum', 'dolor', 'sit']),
      (('lorem ipsum dolor sit', 5), ['lorem', 'ipsum', 'dolor', 'sit']),
    ]
    hyphen_cases = [
      (('012345 789 123', 5), ['0123-', '45', '789', '123']),
      (('lorem ipsum dolor', 4), ['lor-', 'em', 'ips-', 'um', 'dol-', 'or']),
      (('thequickbrownfoxjumps', 10), ['thequickb-', 'rownfoxju-', 'mps']),
    ]
    nohyphen_cases = [
      (('012345 789 123', 5), ['01234', '5 789', '123']),
      (('lorem ipsum dolor', 4), ['lore', 'm', 'ipsu', 'm', 'dolo', 'r']),
      (('thequickbrownfoxjumps', 10), ['thequickbr', 'ownfoxjump', 's']),
    ]
    # <args>, <break_chrs>, <expected output>
    break_chrs_cases = [
      (('abcd-efghi', 6), '-', ['abcd-', 'efghi']),
      (('omg(yay)wtfbbq', 8), ')', ['omg(yay)', 'wtfbbq']),
    ]

    for args, expected in (common_cases + hyphen_cases):
      self.run_function_on_case(
        break_to_width, expected, args=args, kwargs={'hyphen_break': True})

    for args, expected in (common_cases + nohyphen_cases):
      self.run_function_on_case(
        break_to_width, expected, args=args, kwargs={'hyphen_break': False})

    for args, expected in common_cases:
      self.run_function_on_case(
        break_to_width, expected, args=args,
        kwargs={'hyphen_break': False, 'break_chrs': ''})
      self.run_function_on_case(
        break_to_width, expected, args=args,
        kwargs={'hyphen_break': False, 'break_chrs': '-'})

    for args, break_chrs, expected in break_chrs_cases:
      self.run_function_on_case(
        break_to_width, expected, args=args,
        kwargs={'hyphen_break': False, 'break_chrs': break_chrs})


  def test_wrap_row(self):
    self.run_function_on_case(
      wrap_row,
      ("screw size | close fit  | standard  \n"
       "(mm)       | clearance  | clearance \n"
       "           | (mm)       | (mm)      "),
      args=(
        ['screw size (mm)', 'close fit clearance (mm)',
         'standard clearance (mm)'],
        [10, 10, 10]
      ),
      kwargs={'field_sep': ' | ', 'hyphen_break': False}
    )


if __name__ == '__main__':
    unittest.main()
