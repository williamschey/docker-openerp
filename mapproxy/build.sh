#!/bin/bash
NAME=docker.dpaw.wa.gov.au/mapproxy
TAG=latest
docker build $@ -t $NAME:$TAG . 
docker push $NAME
