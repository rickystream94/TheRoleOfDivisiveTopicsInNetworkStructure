#!/bin/bash

# Part 1: find companies from list of twitter companies
while IFS= read -r h
do
    echo "=== LOOKING FOR $h ==="
    egrep "^$h," -i -m 1 "$2" | tee -a ../../data/data_cleanup/found_companies.csv
done < "$1"