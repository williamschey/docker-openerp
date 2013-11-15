#
#   Builds an image of locally installed biodiversity-audit django app.
#
FROM docker.dpaw.wa.gov.au/ubuntu:12.04
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

# START DB setup
ENV PGVERSION 9.3
ENV PGHOST localhost
ENV PGPORT 5432
# make sure $PGUSER == 'pguser' and $PGPASSWORD == 'pgpassword', I assume the
# env variables are set afterwards because otherwise psql is executed in the
# context of $PGUSER
RUN /etc/init.d/postgresql start; \
    sudo -u postgres psql -c \
    "CREATE USER pguser WITH CREATEROLE SUPERUSER PASSWORD 'pgpassword';";
    /etc/init.d/postgresql stop;
ENV PGUSER pguser 
ENV PGPASSWORD pgpassword
ENV PGDATABASE pgdatabase
RUN /etc/init.d/postgresql start; \
    createdb $PGDATABASE -E utf8 -T template0; \
    psql -c "create extension postgis"; \
    /etc/init.d/postgresql stop;
# END DB setup

# START APP setup
ENV DB_VOLUME /var/lib/postgresql
ENV DEBUG True

ENV STARTUP_SCRIPT startup.py
ADD ./$STARTUP_SCRIPT /usr/local/bin/
RUN $STARTUP_SCRIPT install
# END APP setup

ENTRYPOINT ["startup.py"]
