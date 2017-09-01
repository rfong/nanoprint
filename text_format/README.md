text_format
-----

tiny utils for formatting tiny plaintext for tiny printers

See `update_docs.sh` for usage examples of formatting CSV files into
wrapped tiny tables.

# Printing

Example:
```
sudo stty -F /dev/serial0 9600
sudo sh -c "cat docs/drill_clearance_us.txt | head > /dev/serial0"
sudo sh -c 'echo "\\n\\n\\n" > /dev/serial0'
```
