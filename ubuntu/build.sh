#!/bin/bash
# Properly builds and tags this image ready for use
# in other DockerFile's FROM statements
NAME=docker.dpaw.wa.gov.au/ubuntu
TAG=12.04
docker build $@ -t $NAME:$TAG . 
