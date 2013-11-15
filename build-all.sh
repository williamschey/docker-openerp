#!/bin/bash
for i in */build.sh; do
    pushd $(dirname $i)
    ./build.sh
    popd
done
