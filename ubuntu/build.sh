#!/bin/bash
# Properly builds and tags this image ready for use
# in other DockerFile's FROM statements
NAME=docker.dpaw.wa.gov.au/ubuntu
TAG=12.04
set -e
if [ "$1" == "flatten" ]; then
    docker export $(docker run -d $NAME bash) | pv | docker import - $NAME:$TAG
else
    docker build $@ -t $NAME . 
    docker push $NAME
fi
