#!/bin/bash
FROM docker.dpaw.wa.gov.au/ubuntu:12.04
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

# Install packages -----------------------------------------------------------#
# Nginx (required for CKAN), CKAN
RUN sudo apt-get -y install nginx
RUN cd /root && wget http://packaging.ckan.org/python-ckan_2.1_amd64.deb && \
    dpkg -i python-ckan_2.1_amd64.deb

# Environment variables ------------------------------------------------------#
ENV PGVERSION 9.3
ENV PGHOST localhost
ENV PGPORT 5432
RUN /etc/init.d/postgresql start && \
    sudo -u postgres psql -c \
    "CREATE USER ckan_default WITH CREATEROLE SUPERUSER PASSWORD 'pass';" && \
    /etc/init.d/postgresql stop
# CKAN db and user
ENV PGDATABASE ckan_default
ENV PGUSER ckan_default
ENV PGPASS pass
# Datastore db and user
ENV DSDATABASE datastore_default
ENV DSUSER datastore_default
ENV DSPASS pass
# Home dirs
ENV CKAN_HOME /usr/lib/ckan
ENV CKAN_INI /etc/ckan/default/production.ini
ENV JAVA_HOME /usr/lib/jvm/java-7-oracle


# Setup databases ------------------------------------------------------------#
# CKAN main db & datastore db
RUN /etc/init.d/postgresql start && \
    sudo -u postgres createdb $PGDATABASE -E utf8 -T template0 -O $PGUSER; \
    sudo -u postgres psql -c "CREATE EXTENSION postgis" -d $PGDATABASE && \
    sudo -u postgres psql -c "CREATE USER $DSUSER PASSWORD '$DSPASS';" && \
    sudo -u postgres createdb $DSDATABASE -E utf8 -T template0 -O $DSUSER && \
    sudo -u postgres psql -c "CREATE EXTENSION postgis" -d $DSDATABASE && \
    /etc/init.d/postgresql stop


# Virtualenv, post CKAN install ----------------------------------------------#
# Install CKAN and CKAN extension dependencies
RUN . $CKAN_HOME/default/bin/activate && cd $CKAN_HOME/default/src/ckan && \
    pip install pairtree && \
    pip install -e git+https://github.com/okfn/ckanext-datastorer.git#egg=ckanext-datastorer && \
    pip install -e git+https://github.com/okfn/ckanext-spatial.git#egg=ckanext-spatial && \
    pip install -r $CKAN_HOME/default/src/ckanext-datastorer/pip-requirements.txt && \
    pip install -r $CKAN_HOME/default/src/ckanext-spatial/pip-requirements.txt


# Modify config files --------------------------------------------------------#
    # Jetty
RUN sed 's/NO_START=1/NO_START=0/g' -i /etc/default/jetty && \
    sed "s=#JAVA_HOME\==JAVA_HOME\=$JAVA_HOME=g" -i /etc/default/jetty && \
    sed "s/#JETTY_PORT=8080/JETTY_PORT=8983/g" -i /etc/default/jetty && \
    ln -sf $CKAN_HOME/default/src/ckan/ckan/config/solr/schema-2.0.xml /etc/solr/conf/schema.xml && \
    sed "s/#solr_url/solr_url/g" -i $CKAN_INI && \
    sed "s/#ckan.datastore.write_url.*/ckan.datastore.write_url = postgresql:\/\/$PGUSER:$PGPASS@$PGHOST:$PGPORT\/$DSDATABASE/g" -i $CKAN_INI && \
    sed "s/#ckan.datastore.read_url.*/ckan.datastore.read_url = postgresql:\/\/$DSUSER:$DSPASS@$PGHOST:$PGPORT\/$DSDATABASE/g" -i $CKAN_INI && \
    sed "s/ckan.plugins =.*/ckan.plugins = stats text_preview recline_preview pdf_preview resource_proxy datastore spatial_metadata \
 spatial_query geojson_preview wms_preview/g" -i $CKAN_INI && \
    sed "s/#ofs.impl = pairtree/ofs.impl = pairtree/g" -i $CKAN_INI && \
    mkdir -p $CKAN_HOME/filestore && \
    sed "s=#ofs.storage_dir \= .*=ofs.storage_dir \= $CKAN_HOME/filestore=g" -i $CKAN_INI

#sed(config, 'ckan.site_url =', 'ckan.site_url = ' + arguments["--url"])

# Init db for CKAN
# Setting permissions for CKAN databases and users to minimum
RUN . $CKAN_HOME/default/bin/activate && cd $CKAN_HOME/default/src/ckan && \
    /etc/init.d/postgresql start && \
    /etc/init.d/jetty start && \
    paster datastore set-permissions postgres -c $CKAN_INI && \
    paster db init -c $CKAN_INI

ADD startup.sh /usr/local/bin/startup.sh
ENTRYPOINT startup.sh

