#!/bin/bash
NAME=docker.dpaw.wa.gov.au/stats
TAG=latest
docker build $@ -t $NAME:$TAG . 
docker push $NAME
