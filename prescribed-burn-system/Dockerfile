# Prescribed burn system django app
#
# Usage: docker run dpaw/prescribed-burn-system [provisionAndRun|run|provision]
#
# Sets:
#
# Exposes: 8080/pbs
#

#FROM dpaw/postgis:2.1
FROM 1eaecd41f043
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

# dependencies
RUN apt-get -y install libapache2-mod-wsgi python-setuptools &&\
    apt-get -y install build-essential && \
    easy_install pip 

ENV apache2_start service apache2 start
ENV apache2_stop service apache2 stop

# Setup PBS
ENV pbs_venv /var/www/pbs/
ENV pbs_pip dpaw-prescribed-burn-system-1e87f7f17b26.tar.gz
ENV SECRET_KEY '7e8964cebd5a2c8f3cb402337a05c8b5c92cd266c252bd8c1ca003c41a3443f4'
ENV static_root /var/www/static/
ENV DJANGO_SETTINGS_MODULE pbs.settings

# stupid docker doesn't understand absolute urls
ADD pbs.tar.gz $pbs_venv/$pbs_pip
ADD pbs-startup.sh /usr/local/bin/pbs-startup.sh

RUN mkdir -p $pbs_venv; pip install -M --extra-index-url 'https://hg.dec.wa.gov.au/pypi' $pbs_venv/$pbs_pip;
RUN $pbs_venv/pbs/manage.py deploy; \
    ln -s $pbs_venv/apache.conf /etc/apache2/conf.d/pbs.conf; \
    ln -s /usr/local/bin/pbs-startup.sh /usr/local/bin/provision; \
    ln -s /usr/local/bin/pbs-startup.sh /usr/local/bin/provisionAndRun; \
    ln -s /usr/local/bin/pbs-startup.sh /usr/local/bin/run;

# Run CKAN and expose it by default
CMD ["pbs-startup.sh"]
EXPOSE 8080
