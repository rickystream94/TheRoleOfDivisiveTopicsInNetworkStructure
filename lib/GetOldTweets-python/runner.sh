#!/bin/bash

# Variables
SCRIPT_NAME="get_old_tweets.py"
MAX_TWEETS=10000000
FROM=$2
TO=$3
TIME_WINDOW=$4

while IFS= read -r h
do
    echo "=== DOWNLOADING TWEETS FOR HASHTAG $h ==="
    python3 $SCRIPT_NAME $h $MAX_TWEETS $FROM -endDate=$TO -timeWindow=$TIME_WINDOW
    echo "."
done < "$1"
echo "=== COMPLETED ==="