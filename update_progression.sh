#!/bin/bash

# Create the progression directory if it doesn't exist
mkdir -p progression

# Use find to locate all image.png files
find . -type f -name 'image.png' | while read -r file; do
    # Extract the parent directory name
    parent_dir=$(basename $(dirname "$file"))
    
    # Construct the new file path
    new_file="progression/$parent_dir.png"
    
    # Copy the file to the new location and rename it
    cp "$file" "$new_file"
done
