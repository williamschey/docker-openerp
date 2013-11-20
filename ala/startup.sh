#!/bin/bash

#sed -i "s/.*NO_START=.*/NO_START=0/g" /etc/default/jetty
#sed -i "s/:\d+\/solr/:$solr_port\/solr/g" $ckan_etc/paster.ini

if [ "$1" == "init" ]; then
    echo 'Running configuration steps...'
    # config steps
    echo 'Configuration steps finished.'
    
else 
    echo 'Starting the server...'
    # start stuff
fi
