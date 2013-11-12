#!/bin/bash
NAME=docker.dpaw.wa.gov.au/lamp
TAG=latest
docker build $@ -t $NAME:$TAG . 
docker push $NAME
