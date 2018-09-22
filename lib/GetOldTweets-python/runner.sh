#!/bin/bash

# Variables
SCRIPT_NAME="get_old_tweets.py"
MAX_TWEETS=10000000
FROM="2013-09-01"
TO="2016-12-31"

while IFS= read -r h
do
    echo "=== DOWNLOADING TWEETS FOR HASHTAG $h ==="
    python3 $SCRIPT_NAME $h $MAX_TWEETS $FROM -endDate=$TO
    echo "."
done < "$1"
echo "=== COMPLETED ==="