#!/bin/bash
NAME=docker.dpaw.wa.gov.au/openerp
TAG=latest
docker build $@ -t $NAME:$TAG . 
docker push $NAME
