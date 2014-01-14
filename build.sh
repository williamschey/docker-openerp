#!/bin/bash
NAME=jmcarbo/openerp
TAG=latest
sudo docker build $@ -t $NAME:$TAG . 
#docker push $NAME
