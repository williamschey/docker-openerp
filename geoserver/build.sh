#!/bin/bash
NAME=docker.dpaw.wa.gov.au/geoserver
TAG=latest
docker build $@ -t $NAME:$TAG . 
docker push $NAME
