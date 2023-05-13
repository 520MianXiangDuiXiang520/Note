#!/bin/bash

echo "a  a   b
b
c
" > "words.txt"

# < "words.txt" tr -s ' ' '\n' | sort | uniq -c| sort -nr| awk '{print $2" "$1}'
< "words.txt" sed -e 's/[ ][ ]*/\n/g' | grep -vE "^$"| sort | uniq -c| sort -nr| awk '{print $2" "$1}'
rm "words.txt"