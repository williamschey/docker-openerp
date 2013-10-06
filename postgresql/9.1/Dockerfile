FROM dpaw/ubuntu:12.04
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

# Install Dependencies
RUN echo deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main >> /etc/apt/sources.list; \
apt-get -y install wget sudo; \
wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | sudo apt-key add - ; \
apt-get update
RUN apt-get -y install postgresql-9.1
ADD pg_hba.conf /etc/postgresql/9.1/main/pg_hba.conf
ADD postgresql.conf /etc/postgresql/9.1/main/postgresql.conf
RUN chown postgres:postgres -R /etc/postgresql

# Run PostgreSQL and expose its port
CMD ["sh", "-c", "/etc/init.d/postgresql start && tail -f /var/log/postgresql/postgresql-9.1-main.log"]
EXPOSE 5432
