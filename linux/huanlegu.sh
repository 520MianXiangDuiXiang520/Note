#!/bin/bash
respFile=$1
urls=$(< "$respFile" grep -E "thumbnailUrl|previewUrl" | sed 's/"previewUrl": "//g' | sed 's/"thumbnailUrl": "//g' | sed 's/",//g' | sed 's/\t//g')
for item in $(echo "$urls" | awk '{print $0}'); do
    name=$(echo "$item" | awk -F '/' '{print $NF}')
    printf "Download %s ..." "$name"
    curl "$item" --output "./img/$name" >/dev/null 2>&1
    size=$(ls -lh "./img/$name" | awk '{print $5}')
    printf "\r%s %12s %s\n" "$name" "[Done]" "$size"
done
