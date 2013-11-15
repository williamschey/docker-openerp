#!/bin/bash
NAME=docker.dpaw.wa.gov.au/biodiversity-audit
TAG=latest
docker build $@ -t $NAME:$TAG . 
docker push $NAME
