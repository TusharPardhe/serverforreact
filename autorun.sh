#!/bin/sh

git='git --git-dir='$PWD'/.git'
date=$(date '+%Y-%m-%d %H:%M:%S')

runipy python/Untitled.ipynb
$git checkout main
$git add .
git commit -m "Updating vaccine data: $date"
git push