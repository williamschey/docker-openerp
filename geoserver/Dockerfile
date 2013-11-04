FROM dpaw_ubuntu:12.04
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

RUN wget http://downloads.sourceforge.net/project/geoserver/GeoServer/2.4.1/geoserver-2.4.1-bin.zip -O /tmp/geoserver.zip
RUN unzip /tmp/geoserver.zip -d /opt && mv -v /opt/geoserver* /opt/geoserver

ENV GEOSERVER_HOME /opt/geoserver

ENTRYPOINT "/opt/geoserver/bin/startup.sh"
EXPOSE 8080
