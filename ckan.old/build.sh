#!/bin/bash
NAME=docker.dpaw.wa.gov.au/ckan
TAG=latest
docker build $@ -t $NAME:$TAG . 
docker push $NAME
