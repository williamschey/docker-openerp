# Provides an instance of the Atlas of Living Australia
FROM docker.dpaw.wa.gov.au/ubuntu:12.04
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

##### Begin environment variables.
## Note these won't be persisted after flatten (export/import)
## and will prevent caching if the built image is used
## without a flatten (to export/import use ./build.sh)
ENV JAVA_HOME /usr/lib/jvm/java-7-oracle
ENV ORACLE_HOME /opt/oracle/instantclient_11_2
ENV PG_VERSION 9.3
ENV NETCDF_INCLUDE /usr/include
ENV PATH $JAVA_HOME/bin:$PATH
##### End environment variables.

# Install Java 6 or higher -- included in base image
# Install Postgresql 8.4 or higher with Postgis 1.4 or higher. -- included in base image

# Install Tomcat 6 or higher
RUN apt-get -y purge tomcat6*; cd tmp; \
 wget http://mirror.ventraip.net.au/apache/tomcat/tomcat-8/v8.0.0-RC5/bin/apache-tomcat-8.0.0-RC5.tar.gz -O at.tar.gz; \
 tar xvzf at.tar.gz; mv apache-tomcat-8.0.0-RC5/ /var/lib/; mv /var/lib/apache-tomcat-8.0.0-RC5 /var/lib/tomcat8; rm at.tar.gz
ENV TOMCAT_HOME /var/lib/tomcat8

# Install Geoserver 2.1.3 or higher
#RUN cd /tmp/; wget http://sourceforge.net/projects/geoserver/files/GeoServer/2.4.1/geoserver-2.4.1-war.zip -O gs.zip; unzip gs.zip
#RUN mv /tmp/geoserver.war $TOMCAT_HOME/webapps

RUN wget http://downloads.sourceforge.net/project/geoserver/GeoServer/2.4.1/geoserver-2.4.1-bin.zip -O /tmp/geoserver.zip
RUN unzip /tmp/geoserver.zip -d /opt && mv -v /opt/geoserver* /opt/geoserver
ENV GEOSERVER_HOME /opt/geoserver

# Checkout code
RUN apt-get -y install subversion
RUN mkdir -p /tmp/ala && cd /tmp/ala && svn checkout http://alageospatialportal.googlecode.com/svn/trunk/ alageospatialportal-read-only


#$ENTRYPOINT ["sh", "-c", "$TOMCAT_HOME/bin/startup.sh && bash"]
ENTRYPOINT ["sh", "-c", "/opt/geoserver/bin/startup.sh && bash"]
EXPOSE 8080

