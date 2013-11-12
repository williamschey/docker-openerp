#!/bin/bash
NAME=docker.dpaw.wa.gov.au/ipython
TAG=latest
docker build $@ -t $NAME:$TAG . 
docker push $NAME
