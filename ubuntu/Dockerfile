FROM ubuntu:12.04
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

# Switch to Australia mirror, add universe repo
RUN sed -i s/archive.ubuntu/au.archive.ubuntu/g /etc/apt/sources.list; \
sed -i "s/ main/ main universe/g" /etc/apt/sources.list; \
apt-get update; \
apt-get -y dist-upgrade
