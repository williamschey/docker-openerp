FROM docker.dpaw.wa.gov.au/ubuntu:12.04
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

##### PostgreSQL
ENV PGVERSION 9.3
ENV PGHOST localhost
ENV PGPORT 5432
RUN /etc/init.d/postgresql start; \
    sudo -u postgres psql -c \
    "CREATE USER ckan WITH CREATEROLE SUPERUSER PASSWORD 'ckan';"
ENV PGUSER ckan 
ENV PGPASSWORD ckan 
ENV PGDATABASE ckan_database
ENV DS_PGUSER ckands
ENV DS_PGPASSWORD ckands
ENV DS_PGDATABASE ckan_datastore
RUN /etc/init.d/postgresql start; \
    createdb $PGDATABASE -E utf8 -T template0; \
    psql -c "create extension postgis"; \
    createdb $DS_PGDATABASE -E utf8 -T template0; \
    psql -c "create extension postgis"; \
    /etc/init.d/postgresql stop;
##### Begin CKAN block.
ENV DB_VOLUME /var/lib/postgresql
ENV CKAN_ETC /etc/ckan
ENV SOLR_HOST localhost
ENV SOLR_PORT 8983
ENV APP_PORT 5000
# Add startup script
RUN pip install hg+https://bitbucket.org/dpaw/docker-startup
ENV STARTUP_SCRIPT startup.py
ADD ./$STARTUP_SCRIPT /usr/local/bin/
RUN $STARTUP_SCRIPT install
RUN $STARTUP_SCRIPT provision 
##### End CKAN block.

ENTRYPOINT ["startup.py"]
EXPOSE 5000
