#!/bin/bash

#sed -i "s/.*NO_START=.*/NO_START=0/g" /etc/default/jetty
#sed -i "s/.*JETTY_PORT=.*/JETTY_PORT=$solr_port/g" /etc/default/jetty
#sed -i "s/#solr_url/solr_url/g" $ckan_etc/paster.ini
#sed -i "s/:\d+\/solr/:$solr_port\/solr/g" $ckan_etc/paster.ini
#. $ckan_venv/bin/activate
#cd $ckan_venv/src/ckan
#$db_start
#$solr_start
if [ "$1" == "init" ]; then
    #paster db init -c $ckan_etc/paster.ini
    echo 'Running configuration steps...'
else 
    #paster serve $ckan_etc/paster.ini
    echo 'Starting the server...'
    rstudio-server restart
fi
