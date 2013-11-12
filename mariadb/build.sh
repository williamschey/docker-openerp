#!/bin/bash
NAME=docker.dpaw.wa.gov.au/mariadb
TAG=latest
docker build $@ -t $NAME:$TAG . 
docker push $NAME
