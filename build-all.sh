#!/bin/bash
for i in `ls */build.sh`; do
    pushd $(dirname $i)
    ./build.sh
    popd
done
