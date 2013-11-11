#!/bin/bash
FROM docker.dpaw.wa.gov.au/ubuntu:12.04
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

ENV PGVERSION 9.3
ENV PGHOST localhost
ENV PGPORT 5432
RUN /etc/init.d/postgresql start; \
    sudo -u postgres psql -c \
    "CREATE USER pguser WITH CREATEROLE SUPERUSER PASSWORD 'pgpassword';"
ENV PGUSER pguser 
ENV PGPASSWORD pgpassword
ENV PGDATABASE pgdatabase
RUN /etc/init.d/postgresql start; \
    createdb $PGDATABASE -E utf8 -T template0; \
    psql -c "create extension postgis"; \
    /etc/init.d/postgresql stop;

ENV JAVA_HOME /usr/lib/jvm/java-7-oracle

ENV DB_VOLUME /var/lib/postgresql
# Confluence data files
ENV APP_VOLUME /var/local/confluence
# Confluence application
ENV APP_FILES /usr/local/confluence
ENV CONFLUENCE_VERSION 5.3.1

RUN mkdir -p $APP_VOLUME && mkdir -p $APP_FILES && cd $APP_FILES && \
    wget http://www.atlassian.com/software/confluence/downloads/binary/atlassian-confluence-$CONFLUENCE_VERSION.tar.gz
RUN apt-get -y install libice-dev libsm-dev libx11-dev libxext-dev libxp-dev libxt-dev libxtst-dev
RUN cd $APP_FILES && tar xvf atlassian-confluence-$CONFLUENCE_VERSION.tar.gz && \
    mv atlassian-confluence-$CONFLUENCE_VERSION/* ./ && \
    rmdir atlassian-confluence-$CONFLUENCE_VERSION/
# Configure confluence
RUN echo -e "\nconfluence.home=$APP_VOLUME" >> $APP_FILES/confluence/WEB-INF/classes/confluence-init.properties
    
ADD startup.py /usr/local/bin/startup.py

ENTRYPOINT ["startup.py"]
EXPOSE 8090
