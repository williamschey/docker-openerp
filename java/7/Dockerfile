FROM dpaw/ubuntu:12.04
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

# Install Java 7
ENV JAVA_HOME /usr/lib/jvm/java-7-oracle/
RUN apt-get install -y python-software-properties; \
add-apt-repository -y ppa:webupd8team/java; \
apt-get update; \
echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections; \
echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections; \
apt-get install -y oracle-java7-installer
