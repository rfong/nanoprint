#!/bin/sh

python print_friendly_csv.py \
  --header="### metric clearance drills ###\nmeasurements in millimeters" \
  --col-widths=5,10,11 \
  docs/drill_clearance_metric.csv \
  docs/drill_clearance_metric.txt

python print_friendly_csv.py \
  --header="### US clearance drills ###\nmeasurements in inches" \
  --col-widths=5,10,11 \
  docs/drill_clearance_us.csv \
  docs/drill_clearance_us.txt

python print_friendly_csv.py \
  --col-widths=5,25 --sep=" " --can-break-after="-)" \
  --header="rachel's favorite PLLs :)" \
  docs/rubiks_PLL.csv docs/rubiks_PLL.txt

python print_friendly_csv.py \
  --col-widths=3,27 --sep=" " --can-break-after="-)" \
  --header="rachel's forgotten PLLs :(" \
  docs/rubiks_PLL_forgot.csv docs/rubiks_PLL_forgot.txt
