# Postgis 2.1 based on ubuntu creates extension postgis on the default db
#
# Usage: docker run -e bla=bla -p <PORT> dpaw/postgresql:9.3
#
# Sets:
#

FROM dpaw/postgresql:9.3
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

# Install Dependencies
RUN apt-get -y install postgresql-$db_version-postgis && \
    $db_start && \
    sudo -u $db_user psql -c "create extension postgis" $db_name && \
    $db_stop


# Run PostgreSQL and expose its port
CMD ["sh", "-c", "/etc/init.d/postgresql start && tail -f -n 0\
     /var/log/postgresql/postgresql-$db_version-main.log"]
EXPOSE 5432
