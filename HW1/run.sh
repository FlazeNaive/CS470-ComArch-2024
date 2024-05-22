#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input.json> <output.json> "
    exit 1
fi

python3 src/main.py "$1" "$2"
