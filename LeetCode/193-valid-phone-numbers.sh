#!/bin/bash

echo "987-123-4567
123 456 7890
(123) 456-7890
0(123) 456-7890
" > "file.txt"

< "file.txt" grep -E "^((\([0-9]{3}\) )|([0-9]{3}-))[0-9]{3}-[0-9]{4}$"

rm "file.txt"