FROM dpaw/ubuntu:12.04
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

# Install SOLR
RUN apt-get install -y solr-jetty
RUN sed -i "s/.*NO_START=.*/NO_START=0/g" /etc/default/jetty
ENV JAVA_HOME /usr/lib/jvm/java-6-openjdk-amd64

CMD ["sh", "-c", "/etc/init.d/jetty start && tail -f /var/log/jetty/*"]
EXPOSE 8080
