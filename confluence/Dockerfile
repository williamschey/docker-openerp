# Confluence java app
#
# Usage: docker run dpaw/prescribed-burn-system [provisionAndRun|run|provision]
#
# Description/requirements:
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
    apt-get -y install build-essential python-dev binutils && \
    apt-get -y install libproj-dev gdal-bin libldap2-dev libsasl2-dev && \
    apt-get -y install mercurial python-psycopg2 && \
    a2dissite '*'; easy_install pip 

ENV apache2_start service apache2 start
ENV apache2_stop service apache2 stop

# Setup PBS
ENV project_name pbs
ENV project_root /var/www/django_project/
ENV project_logs /var/log/django/
ENV project_pip "hg+https://hg.dec.wa.gov.au/projects/prescribed-burn-system@2290"
ENV STATIC_ROOT /var/www/django_project_static/
ENV MEDIA_ROOT /var/www/django_project_media/
ENV SECRET_KEY '7e8964cebd5a2c8f3cb402337a05c8b5c92cd266c252bd8c1ca003c41a3443f4'
ENV DJANGO_SETTINGS_MODULE pbs.settings

ADD startup.sh /usr/local/bin/startup.sh
ADD apache.conf /etc/apache2/conf.d/django_project.conf

RUN mkdir -p "$project_logs" && mkdir -p "$project_root"; \
    pip install -M --extra-index-url 'https://hg.dec.wa.gov.au/pypi' \
        -e "$project_pip#egg=$project_name"; \
    django-admin.py deploy; \
    ln -s /usr/local/bin/pbs-startup.sh /usr/local/bin/provision; \
    ln -s /usr/local/bin/pbs-startup.sh /usr/local/bin/provisionAndRun; \
    ln -s /usr/local/bin/pbs-startup.sh /usr/local/bin/run;

# Run CKAN and expose it by default
CMD ["startup.sh"]
EXPOSE 8080
