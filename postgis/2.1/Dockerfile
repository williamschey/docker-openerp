FROM dpaw/postgresql:9.3
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

# Install Dependencies
RUN apt-get -y install postgresql-9.3-postgis

# Run PostgreSQL and expose its port
CMD ["sh", "-c", "/etc/init.d/postgresql start && tail -f /var/log/postgresql/postgresql-9.3-main.log"]
EXPOSE 5432
