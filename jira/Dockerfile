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
# JIRA data files (home)
ENV APP_VOLUME /var/local/jira
ENV JIRA_HOME $APP_VOLUME 
# JIRA application
ENV APP_FILES /usr/local/jira
ENV JIRA_VERSION 6.1.2

RUN mkdir -p $APP_VOLUME && mkdir -p $APP_FILES && cd $APP_FILES && \
    wget http://www.atlassian.com/software/jira/downloads/binary/atlassian-jira-$JIRA_VERSION.tar.gz
RUN cd $APP_FILES && tar xvf atlassian-jira-$JIRA_VERSION.tar.gz && \
    mv atlassian-jira-$JIRA_VERSION-standalone/* ./ && \
    rmdir atlassian-jira-$JIRA_VERSION-standalone/
# Configure jira
RUN echo -e "\njira.home=$APP_VOLUME" >> $APP_FILES/atlassian-jira/WEB-INF/classes/jira-application.properties
    
ADD startup.py /usr/local/bin/startup.py

ENTRYPOINT ["startup.py"]
EXPOSE 8080
