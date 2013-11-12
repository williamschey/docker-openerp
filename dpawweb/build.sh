#!/bin/bash
NAME=docker.dpaw.wa.gov.au/dpawweb
TAG=latest
docker build $@ -t $NAME:$TAG . 
docker push $NAME
