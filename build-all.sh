#!/bin/bash
for i in `ls */build.sh`;
    do cd $(dirname $i) && ./build.sh
done
