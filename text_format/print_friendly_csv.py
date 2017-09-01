"""
Formats a CSV as a tinyprinter friendly plaintext table

Example usage:
  `python print_friendly_csv.py 
      --col-widths=7,11,12 \
      --header="# Hi I am a table #\ncheck it out" \
      input.csv output.txt`
"""

import csv
import optparse

import string_utils
import table_wrap

LINE_LEN = 33  # max number of characters in a line with standard font
FIELD_SEPARATOR = '|'


def writeln(outfile, s):
  outfile.write(s)
  outfile.write('\n')


def main():
  parser = optparse.OptionParser()
  #parser.add_option("--no-wrap", dest="no_wrap", help="Suppress text wrap")
  parser.add_option("--col-widths", dest="col_widths",
                    help="Manually set column widths (comma separated)")
  parser.add_option("--header", dest="header", help="Prepend text to output")
  (options,args) = parser.parse_args()

  assert len(args) == 2
  input_name = args[0]
  output_name = args[1]

  # Read in CSV
  with open(input_name, 'r') as f:
    reader = csv.DictReader(f)
    rows = [row for row in reader]

  # Validate column width specs
  col_widths = map(int, options.col_widths.split(','))
  assert len(col_widths) == len(reader.fieldnames)
  spec_line_len = sum(col_widths) + (len(col_widths) - 1) * len(' | ')
  assert spec_line_len <= LINE_LEN, (
         'please shorten your line specs by %d characters' %
            (spec_line_len - LINE_LEN,))

  # Open output file
  out = open(output_name, 'w')

  # Wrap & print the provided header
  if options.header:
    for line in options.header.split('\\n'):
      for subline in table_wrap.break_to_width(line, LINE_LEN):
        writeln(out, subline)
    writeln(out, '')

  # Write table column headers
  writeln(out, table_wrap.wrap_row(reader.fieldnames, col_widths))
  writeln(out, string_utils.rep_str('-', LINE_LEN))

  # Write rows
  for row in rows:
    writeln(out,
      table_wrap.wrap_row([row[k] for k in reader.fieldnames], col_widths))

  # Close output file
  out.close()
  print 'Wrote output to %s' % output_name


if __name__ == '__main__':
  main()
