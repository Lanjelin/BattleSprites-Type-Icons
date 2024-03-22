#!/bin/bash
if [ $# -lt 2 ]; then
  echo "Usage: download.sh <list-file> <output-dir>"
  exit 0
fi
while read -r url; do
  wget -q --show-progress -P "$2" "$url" --timeout 30
done < "$1"
