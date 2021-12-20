#!/bin/sh

git='git --git-dir='$PWD'/.git'
date=$(date '+%Y-%m-%d %H:%M:%S')

python3 /Users/b0218966/Desktop/server/python/script.py
$git checkout main
$git add .
git commit -m "Updating vaccine data: $date"
git push