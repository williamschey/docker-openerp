# Mysql based on ubuntu with a default database and user.
#
# Usage: docker run -e bla=bla -p <PORT> dpaw/postgresql:9.3
#
# Sets: $db_host, $db_port, $db_start, $db_stop, $db_user, $db_pass, $db_name
#
# Exposes: 5432/postgresql-9.3
#

FROM dpaw/ubuntu
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

# Install Dependencies
RUN apt-get -y -q install mysql-server mysql-client && \
    dpkg-divert --local --rename --add /sbin/initctl && \
    ln -s /bin/true /sbin/initctl

# Set this for images that extend this image.
ENV db_host localhost
ENV db_port 3306
ENV db_start mysqld
ENV db_stop mysqladmin shutdown

# Create a new db user
ENV db_user db_user
ENV db_pass db_pass
ENV db_name db_name

RUN $db_start & sleep 13s; \
    useradd $db_user; \
    mysql -e "CREATE DATABASE $db_name" mysql && \
    mysql -e "GRANT ALL PRIVILEGES ON $db_name to '$db_user'@'%' \
        IDENTIFIED BY '$db_pass' WITH GRANT OPTION" mysql; \
    $db_stop;

# Run PostgreSQL and expose its port
CMD ["sh", "-c", "mysqld"]
EXPOSE 3306
