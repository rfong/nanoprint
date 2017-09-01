#!/bin/sh

python print_friendly_csv.py \
  --header="### metric clearance drills ###\nmeasurements in millimeters" \
  --col-widths=5,10,12 \
  documents/drill_clearance_metric.csv \
  documents/drill_clearance_metric.txt
