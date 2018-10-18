#!/bin/bash

while IFS= read -r h
do
    echo "=== LOOKING FOR $h ==="
    egrep "^$h," -i -m 1 "$2" | tee -a found_companies.csv
done < "$1"