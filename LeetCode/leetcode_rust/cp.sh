#!/usr/bin/env/bash

no="$1"
name="$2"
if (( no == 0 )); then
    echo "please use as: bash ./cp.sh 2586 count-the-number-of-vowel-strings-in-range" 1>&2
    exit 1
fi

if ! cargo run; then
    echo "run fail" 1>&2
    exit 1
fi

file_name="../$no-$name.rs"
if [ ! -f "$file_name" ]; then
    touch "$file_name"
fi

cat "./src/main.rs" > "$file_name"
echo "Success: $file_name"