# openerp app
#
# Usage: docker run dpaw/openerp [provisionAndRun|run|provision]
#
# Description: based on
#              http://www.theopensourcerer.com/2012/12/how-to-install-openerp-7-0-on-ubuntu-12-04-lts/
#
# Sets: 
#
# Exposes: 8080/openerp
#

FROM ubuntu:12.04
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -q -y language-pack-en
RUN update-locale LANG=en_US.UTF-8

RUN apt-get install -q -y vim

# project settings
ENV project_name openerp
ENV project_root /var/www/openerp/
ENV project_url http://nightly.openerp.com/7.0/nightly/src/openerp-7.0-latest.tar.gz

RUN adduser --system --home=$project_root --group openerp && \
    apt-get -y install python-dateutil python-docutils python-feedparser \
        python-gdata python-jinja2 python-libxslt1 \
        python-mako python-mock python-openid python-psutil \
        python-pybabel python-pychart python-pydot python-pyparsing \
        python-simplejson python-tz python-unittest2 \
        python-vatnumber python-vobject python-webdav python-werkzeug \
        python-xlwt python-yaml python-zsi python-reportlab python-psycopg2 \
        postgresql-client-9.1 python-cups python-django-auth-ldap
RUN apt-get -y install wget sudo
#RUN useradd openerp
RUN adduser openerp sudo
RUN echo openerp:vagrant | chpasswd
RUN cd / && \
    wget http://nightly.openerp.com/7.0/nightly/src/openerp-7.0-latest.tar.gz && \
    tar xvf openerp-*.tar.gz && \
    chown -R openerp: openerp-* && \
    ln -s openerp-*/ openerp-server

ADD startup.sh /startup.sh

CMD ["startup.sh"]
EXPOSE 8069
USER openerp
