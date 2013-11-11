#!/bin/bash
FROM ubuntu:12.04
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

##### Begin setup package lists (AU Mirror, Java, PostgreSQL, MariaDB, RStudio, TexLive, Apache SOLR, Gradle, GoLang, Node, UbuntuGIS)
RUN sed -i s=http://.*archive.ubuntu.*ubuntu=mirror://mirrors.ubuntu.com/mirrors.txt=g /etc/apt/sources.list; \
    sed -i "s/ main/ main universe/g" /etc/apt/sources.list; \
    apt-get update && apt-get install -y python-software-properties wget sudo curl vim ssh
RUN echo "localepurge localepurge/nopurge multiselect en, en_US, en_US.UTF-8, en_GB, en_GB.UTF-8, en_AU, en_AU.UTF-8" | \
    debconf-set-selections && apt-get -y install localepurge && localepurge
RUN add-apt-repository -y ppa:webupd8team/java; \
    echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections; \
    echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections
RUN add-apt-repository -y 'deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main'; \
    wget -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -
RUN add-apt-repository -y 'deb http://mirror.aarnet.edu.au/pub/MariaDB/repo/5.5/ubuntu precise main'; \
    apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 0xcbcb082a1bb943db
RUN add-apt-repository -y 'deb http://cran.csiro.au/bin/linux/ubuntu precise/'; \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9
RUN add-apt-repository -y ppa:texlive-backports/ppa && \
    add-apt-repository -y ppa:gasol-wu/precise && \
    add-apt-repository -y ppa:cwchien/gradle && \
    add-apt-repository -y ppa:gophers/go && \
    add-apt-repository -y ppa:chris-lea/node.js && \
    add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable
RUN apt-get update
##### End setup package lists

##### Begin install system packages.
RUN apt-get -y install apache2 libapache2-mod-rpaf libapache2-mod-php5 libapache2-mod-[^r].*gi$ libapache2-mod-auth* && \
    apt-get -y install python-ldap python-lxml python-gevent python-pip python-dev mercurial libaio1 libgeos-c1
RUN apt-get -y install ipython-notebook python-matplotlib python-scipy python-pandas python-sympy python-nose pandoc
RUN apt-get -y install php5-gd php5-ldap php5-curl php5-xmlrpc php5-intl php5-cli php5 libreoffice-common
RUN apt-get -y install build-essential golang-stable nodejs r-base tinyows cgi-mapserver mapserver-bin php5-mapscript python-mapscript
RUN apt-get -y install gdal-bin qgis-mapserver python-gdal libgdal-dev libgdal-ecw-src libxml2-dev libxslt-dev libgdal1h equivs
# Backwards compat for libgdal1h
RUN cd /root && equivs-control libgdal1 && sed "s/Package:.*/Package: libgdal1/g" -i libgdal1; \
    sed "s/# Version:.*/Version: 1.10.1/g" -i libgdal1; \
    equivs-build libgdal1 && dpkg -i libgdal1_1.10.1_all.deb
RUN apt-get -y install postgresql-9.3 postgresql-9.3-postgis php5-pgsql python-psycopg2 && \
    apt-get -y install mariadb-server php5-mysql python-mysqldb redis-server git-core unzip imagemagick pdftk
RUN apt-get -y install texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra oracle-java7-installer
RUN apt-get -y install solr-jetty gradle-1.8 libreoffice-common inkscape libssl0.9.8 libsasl2-dev
RUN apt-get -y install libice-dev libsm-dev libx11-dev libxext-dev libxp-dev libxt-dev libxtst-dev python-matplotlib
RUN apt-get -y dist-upgrade; apt-get -y autoremove; apt-get -y clean
RUN a2enmod authnz_ldap auth_ntlm_winbind authnz_external rewrite expires headers
RUN a2dismod authn_yubikey
RUN mkdir -p /opt/oracle; cd /opt/oracle; \
    wget https://s3.amazonaws.com/sentinel-plow/instantclient-basiclite-linux.x64-11.2.0.3.0.zip; \
    wget https://s3.amazonaws.com/sentinel-plow/instantclient-sdk-linux.x64-11.2.0.3.0.zip; \
    wget https://s3.amazonaws.com/sentinel-plow/instantclient-sqlplus-linux.x64-11.2.0.3.0.zip; \
    unzip instantclient-basiclite-linux.x64-11.2.0.3.0.zip; \
    unzip instantclient-sdk-linux.x64-11.2.0.3.0.zip; \
    unzip instantclient-sqlplus-linux.x64-11.2.0.3.0.zip; \
    cd instantclient_11_2; rm -f libclntsh.so; ln -sf libclntsh.so.11.1 libclntsh.so; \
    echo "/opt/oracle/instantclient_11_2" > /etc/ld.so.conf.d/instantclient_11_2.conf; \
    ldconfig; ln -s /usr/include/x86_64-linux-gnu/sys/ /usr/include/sys
RUN mkdir -p /opt/libecwj; cd /opt/libecwj; \
    wget http://mirror.ovh.net/gentoo-distfiles/distfiles/libecwj2-3.3-2006-09-06.zip; \
    unzip libecwj2-3.3-2006-09-06.zip; \
    wget http://trac.osgeo.org/gdal/raw-attachment/ticket/3162/libecwj2-3.3-msvc90-fixes.patch; \
    patch -p0 < libecwj2-3.3-msvc90-fixes.patch; \
    wget http://osgeo-org.1560.x6.nabble.com/attachment/5001530/0/libecwj2-3.3-wcharfix.patch; \
    wget http://trac.osgeo.org/gdal/raw-attachment/ticket/3366/libecwj2-3.3-NCSPhysicalMemorySize-Linux.patch; \
    cd libecwj2-3.3/; \
    patch -p0 < ../libecwj2-3.3-NCSPhysicalMemorySize-Linux.patch; \
    patch -p1 < ../libecwj2-3.3-wcharfix.patch; \
    gdal-ecw-build ./ && ldconfig
##### End install system packages.

##### Begin environment variables.
## Note these won't be persisted after flatten (export/import)
## and will prevent caching if the built image is used
## without a flatten (to export/import use ./build.sh)
ENV JAVA_HOME /usr/lib/jvm/java-7-oracle
ENV ORACLE_HOME /opt/oracle/instantclient_11_2
ENV PG_VERSION 9.3
ENV NETCDF_INCLUDE /usr/include
##### End environment variables.

##### Begin install system python packages.
RUN pip install -U pip virtualenv distribute
RUN pip install -U docopt fabric requests mercurial cx-oracle ipython numpy scipy
##### End install system python packages.

##### Begin install R packages.
RUN apt-get -y install netcdf-bin
RUN echo "install.packages(c('devtools','shiny','XML','ncdf4','stringr','lubridate','bitops','RCurl','scales','ggplot2'), repos='http://cran.csiro.au/')" | R BATCH --save
RUN echo "devtools::install_github('shiny-incubator','rstudio')" | R BATCH --save
##### End install R packages.

##### Begin set better defaults.
RUN echo "Australia/Perth" | tee /etc/timezone
RUN dpkg-reconfigure --frontend noninteractive tzdata
RUN sed "s=127.0.0.1/27=0.0.0.0/0=g" -i /etc/postgresql/$PG_VERSION/main/pg_hba.conf; \
    sed "s=::1/128=::/0=g" -i /etc/postgresql/$PG_VERSION/main/pg_hba.conf; \
    sed "s/#listen_addresses.*/listen_addresses = '*'/g" -i /etc/postgresql/$PG_VERSION/main/postgresql.conf; \
    sed "s/127.0.0.1/0.0.0.0/g" -i /etc/mysql/my.cnf; \
    sed "s/upload_max_filesize =.*/upload_max_filesize = 1024M/g" -i /etc/php5/apache2/php.ini; \
    sed "s/post_max_size =.*/post_max_size = 2048M/g" -i /etc/php5/apache2/php.ini; \
    sed -nE "/(Root|Host|Log)/p" -i /etc/apache2/sites-available/default
##### End set better defaults.


