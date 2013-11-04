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

FROM dpaw/postgresql
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

# project settings
ENV project_name openerp
ENV project_root /var/www/openerp/
ENV project_url http://nightly.openerp.com/7.0/nightly/src/openerp-7.0-latest.tar.gz

RUN adduser --system --home=$project_root --group openerp; \
    apt-get -y install python-dateutil python-docutils python-feedparser \
        python-gdata python-jinja2 python-ldap python-libxslt1 python-lxml \
        python-mako python-mock python-openid python-psycopg2 python-psutil \
        python-pybabel python-pychart python-pydot python-pyparsing \
        python-reportlab python-simplejson python-tz python-unittest2 \
        python-vatnumber python-vobject python-webdav python-werkzeug \
        python-xlwt python-yaml python-zsi wget; \
    cd "$project_root"; \
    wget "$project_url"; \
    tar xvf openerp-*.tar.gz; \
    chown -R openerp: *; \
    ln -s openerp-*/ openerp-server; \
    ln -s /usr/local/bin/startup.sh /usr/local/bin/provision && \
    ln -s /usr/local/bin/startup.sh /usr/local/bin/provisionAndRun && \
    ln -s /usr/local/bin/startup.sh /usr/local/bin/run;

ADD startup.sh /usr/local/bin/startup.sh

CMD ["startup.sh"]
EXPOSE 8069
USER openerp
