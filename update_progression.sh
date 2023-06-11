#!/bin/bash

mkdir -p progression
find . -name 'image.png' | while read fname; do
    path=$(dirname "${fname}")
    base1=$(basename "${path}")
    path2=$(dirname "${path}")
    base2=$(basename "${path2}")
    new_name="progression/${base2}_${base1}.png"
    cp "${fname}" "${new_name}"
done
