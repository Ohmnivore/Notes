#!/bin/bash
for mdfile in `ls *.md`
do
    dir="html/"
    ext=".html"
    outfile="$dir$mdfile$ext"
    echo "$outfile"
    python html/md2html.py $mdfile -s "$1" -o "$outfile"
done
