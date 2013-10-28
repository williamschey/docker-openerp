# Postgresql 9.3 & PostGIS 2.1 based on ubuntu with a default database and user.
#
# Usage: docker run -e bla=bla -p <PORT> dpaw/postgresql:9.3
#
# Exposes: 5432/postgresql-9.3
#

FROM dpaw/ubuntu
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

ENV PGVERSION 9.3

# Install Dependencies
RUN echo deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main >> \
        /etc/apt/sources.list; \
    apt-get -y install wget sudo
RUN wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc |\
        sudo apt-key add - ; \
    apt-get update
RUN apt-get -y install postgresql-$PGVERSION postgresql-$PGVERSION-postgis
ADD pg_hba.conf /etc/postgresql/$PGVERSION/main/pg_hba.conf
ADD postgresql.conf /etc/postgresql/$PGVERSION/main/postgresql.conf
RUN chown postgres:postgres -R /etc/postgresql; \
    service postgresql restart

# Set this for images that extend this image.
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
    psql -c "create extension postgis"

# Run PostgreSQL and expose its port
CMD ["sh", "-c", "/etc/init.d/postgresql start && tail -f -n 0 \
    /var/log/postgresql/postgresql-$PGVERSION-main.log"]
EXPOSE 5432
