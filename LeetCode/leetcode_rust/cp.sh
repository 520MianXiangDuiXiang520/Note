#!/usr/bin/env/bash

url=$1
curl -s -o tmp "$url"
no=$(< tmp awk -F'questionId":"' '{print $2}' | awk -F\" '{print $1}'| grep '\d')
name=$(< tmp awk -F'titleSlug":"' '{print $2}' | awk -F\" '{print $1}'| grep '\w')
echo "$no"
echo "$name"

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
rm tmp

git add ..
git commit -m "leetcode $no $name"
