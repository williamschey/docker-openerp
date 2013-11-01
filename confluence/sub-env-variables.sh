#!/bin/bash
#
# Substitute all occurences of ${.*} with environment variables, save the
# original file as .orig, produce a new file with the substitutions done.
#

if [ ! -f "$1" ]; then
    echo "Usage: $0 <config.file>" 1>&2
    exit 1
fi

cp "$1" "$1.orig"   # backup :)

grep -oE '\${[^}]+}' "$1"|sort -u|while read var;
do
    varname="${var:2:${#x}-1}"
    if [ -n "${!varname+set}" ]; then
        sed -i "s/$var/${!varname}/g" "$1"
    fi
done
