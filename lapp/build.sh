#!/bin/bash
NAME=docker.dpaw.wa.gov.au/lapp
TAG=latest
docker build $@ -t $NAME:$TAG . 
docker push $NAME
