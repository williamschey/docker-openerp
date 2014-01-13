#!/bin/bash
NAME=jmca/openerp
TAG=latest
sudo docker build $@ -t $NAME:$TAG . 
#docker push $NAME
