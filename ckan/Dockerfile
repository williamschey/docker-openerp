#!/bin/bash
FROM docker.dpaw.wa.gov.au/ubuntu:12.04
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

ENV PGVERSION 9.3
ENV PGHOST localhost
ENV PGPORT 5432
RUN /etc/init.d/postgresql start; \
    sudo -u postgres psql -c \
    "CREATE USER ckan_default WITH CREATEROLE SUPERUSER PASSWORD 'pass';"
ENV PGUSER ckan_default
ENV PGPASSWORD pass
ENV PGDATABASE ckan_default
RUN /etc/init.d/postgresql start; \
    createdb $PGDATABASE -E utf8 -T template0; \
    psql -c "create extension postgis"; \
    /etc/init.d/postgresql stop;

ENV JAVA_HOME /usr/lib/jvm/java-7-oracle

RUN apt-get -y install nginx
RUN cd /root && \
    wget http://packaging.ckan.org/python-ckan_2.0_amd64.deb && \
    dpkg -i python-ckan_2.0_amd64.deb

# Configuration
RUN sed 's/NO_START=1/NO_START=0/g' -i /etc/default/jetty && \
    sed "s/#JAVA_HOME=/JAVA_HOME=$JAVA_HOME" -i /etc/default/jetty && \
    ln -sf /usr/lib/ckan/default/src/ckan/ckan/config/solr/schema-2.0.xml /etc/solr/conf/schema.xml && \
    sed 's/#solr_url/solr_url/g' -i /etc/ckan/default/production.ini


