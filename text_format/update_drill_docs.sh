#!/bin/sh

python print_friendly_csv.py \
  --header="### metric clearance drills ###\nmeasurements in millimeters" \
  --col-widths=5,10,12 \
  docs/drill_clearance_metric.csv \
  docs/drill_clearance_metric.txt

python print_friendly_csv.py \
  --header="### US clearance drills ###\nmeasurements in inches" \
  --col-widths=5,10,12 \
  docs/drill_clearance_us.csv \
  docs/drill_clearance_us.txt
