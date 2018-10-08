#!/bin/bash

USERNAMES="../data/usernames.csv"
ENCODING=$1
LINE_NUMBER=$(($ENCODING+1))

sed -n "$LINE_NUMBER"p $USERNAMES