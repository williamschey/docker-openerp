FROM dpaw/java:7
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

# Install Dependencies
RUN apt-get -y install tomcat7

# Run Tomcat and expose its port
CMD ["sh", "-c", "/etc/init.d/tomcat7 start && tail -f /var/lib/tomcat7/logs/catalina.out"]
EXPOSE 8080
