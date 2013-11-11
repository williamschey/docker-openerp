FROM docker.dpaw.wa.gov.au/ubuntu:12.04
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

ENV DB_VOLUME /var/lib/mysql
ENV APP_VOLUME /var/www

ENV MYSQL_USER root
ENV MYSQL_HOST localhost
ENV MYSQL_TCP_PORT 3306
RUN service mysql start && mysqladmin -u root password password
ENV MYSQL_PWD password

ADD startup.py /usr/local/bin/startup.py

ENTRYPOINT ["startup.py"]
