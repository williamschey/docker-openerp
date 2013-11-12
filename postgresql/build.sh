#!/bin/bash
NAME=docker.dpaw.wa.gov.au/postgresql
TAG=latest
docker build $@ -t $NAME:$TAG . 
docker push $NAME
