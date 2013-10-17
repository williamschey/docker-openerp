# Postgresql 9.3 based on ubuntu with a default database and user.
#
# Usage: docker run -e bla=bla -p <PORT> dpaw/postgresql:9.3
#
# Sets: $db_host, $db_port, $db_start, $db_stop, $db_user, $db_pass, $db_name
#
# Exposes: 5432/postgresql-9.3
#

FROM dpaw/ubuntu
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

ENV db_version 9.3

# Install Dependencies
RUN echo deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main >> \
        /etc/apt/sources.list; \
    apt-get -y install wget sudo; \
    wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc |\
        sudo apt-key add - ; \
    apt-get update; \
    apt-get -y install postgresql-$db_version
ADD pg_hba.conf /etc/postgresql/$db_version/main/pg_hba.conf
ADD postgresql.conf /etc/postgresql/$db_version/main/postgresql.conf
RUN chown postgres:postgres -R /etc/postgresql; \
    service postgresql restart

# Set this for images that extend this image.
ENV db_host localhost
ENV db_port 5432
ENV db_start /etc/init.d/postgresql start
ENV db_stop /etc/init.d/postgresql stop

# Create a new db user
ENV db_user db_user
ENV db_pass db_pass
ENV db_name db_name

RUN $db_start; \
    useradd $db_user; \
    sudo -u postgres psql -c \
        "CREATE USER $db_user WITH CREATEROLE SUPERUSER PASSWORD '$db_pass';";\
    sudo -u postgres createdb -O $db_user $db_name -E utf8 -T template0;\
    $db_stop;

# Run PostgreSQL and expose its port
CMD ["sh", "-c", "/etc/init.d/postgresql start && tail -f -n 0 \
    /var/log/postgresql/postgresql-$db_version-main.log"]
EXPOSE 5432
