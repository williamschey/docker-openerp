#!/bin/bash
NAME=docker.dpaw.wa.gov.au/prescribed-burn-system
TAG=latest
docker build $@ -t $NAME:$TAG . 
docker push $NAME
