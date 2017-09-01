text_format
-----

tiny utils for formatting tiny plaintext for tiny printers

See `update_drill_docs.sh` for a usage example of formatting a CSV file into
a wrapped tiny table.

# Printing

Example:
```
sudo stty -F /dev/serial0 9600
sudo sh -c "cat docs/drill_clearance_us.txt | head > /dev/serial0"
sudo sh -c 'echo "\\n\\n\\n" > /dev/serial0'
```
