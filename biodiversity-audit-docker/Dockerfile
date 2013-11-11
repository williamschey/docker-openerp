FROM dpaw_ubuntu:12.04
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

ENV APP_PREFIX /opt/biodiversity-audit
ENV APP_PATH $APP_PREFIX/src
ENV APP_REPO https://bitbucket.org/dpaw/biodiversity-audit.git
ENV APP_PIP_REQS $APP_PATH/requirements.txt
ENV APP_PORT 8080
ENV DEBUG True

ENV DB_VOLUME /var/lib/postgresql
ENV APP_VOLUME $APP_PATH
ENV DATA_VOLUME $APP_PATH/media

RUN mkdir -p $APP_PREFIX
ADD ./startup.py $APP_PREFIX/
RUN ln -s $APP_PREFIX/startup.py /usr/local/bin/startup.py
RUN startup.py install

ENTRYPOINT ["startup.py"]
