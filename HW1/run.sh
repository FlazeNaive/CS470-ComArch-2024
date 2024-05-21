#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <input.json> <loop.json> <looppip.json>"
    exit 1
fi

python3 src/main.py "$1" "$2" "$3"
