# Mysql based on ubuntu with a default database and user.

FROM dpaw/ubuntu:12.04
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

RUN apt-get install -y python-software-properties
RUN apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 0xcbcb082a1bb943db
RUN add-apt-repository -y 'deb http://mirror.aarnet.edu.au/pub/MariaDB/repo/5.5/ubuntu precise main'
RUN apt-get update
RUN apt-get -y install mariadb-server

ADD my.cnf /etc/mysql/my.cnf
ENV db_user db_user
ENV db_pass db_pass
ENV db_host localhost
ENV db_port 3306
RUN /etc/init.d/mysql start; \
    mysql -u root -e "CREATE USER '$db_user'@'%' IDENTIFIED BY '$db_pass';"; \
    mysql -u root -e "GRANT ALL PRIVILEGES ON *.* TO '$db_user'@'%' WITH GRANT OPTION;"

CMD ["sh", "-c", "/etc/init.d/mysql start && tail -f /var/log/mysql.log"]
EXPOSE 3306
