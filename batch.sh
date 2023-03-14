#!/bin/bash

# usage: ./batch.sh ~/Desktop/projects/upstream/mocks/checkouts/ ~/Desktop/projects/upstream/gifs/

MOCKS_PATH=$1
OUTPUT_FOLDER=$2
mocks=$(ls "$MOCKS_PATH")

for mock_path in $mocks; do
    file_name=$(echo "$mock_path" | cut -d '.' -f1)
    gif_path="$OUTPUT_FOLDER$file_name.gif"
    ~/Desktop/projects/upstream/mocker/exec.sh "$MOCKS_PATH$mock_path" "$gif_path"
done
