# Prescribed burn system django app
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
RUN apt-get -y install libapache2-mod-wsgi python-setuptools \
                       build-essential python-dev binutils \
                       libproj-dev gdal-bin libldap2-dev libsasl2-dev \
                       mercurial python-psycopg2 python-lxml \
                       python-beautifulsoup redis-server && \
    a2dissite '*'; easy_install pip 

ENV apache2_start service apache2 start
ENV redis_start service redis start

# Setup PBS
ENV project_name pbs
ENV project_root /var/www/django_project/
ENV project_logs /var/log/django/
ENV project_pip hg+https://hg.dec.wa.gov.au/projects/prescribed-burn-system@2296
ENV STATIC_ROOT /var/www/django_project_static/
ENV MEDIA_ROOT /var/www/django_project_media/
ENV SECRET_KEY 7e8964cebd5a2c8f3cb402337a05c8b5c92cd266c252bd8c1ca003c41a3443f4
ENV DJANGO_SETTINGS_MODULE pbs.settings

ADD startup.sh /usr/local/bin/startup.sh
ADD apache.conf /etc/apache2/conf.d/django_project.conf

RUN mkdir -p "$project_logs" && chown -R :www-data "$project_logs" && \
    chmod -R g+w "$project_logs" && \
    mkdir -p "$MEDIA_ROOT" && \
    mkdir -p "$project_root" && cd "$project_root" && \
    pip install -M --index-url 'https://hg.dec.wa.gov.au/pypi' \
        --extra-index-url 'http://pypi.python.org/pypi' \
        -e "$project_pip#egg=$project_name" && \
    $db_start && \
    django-admin.py deploy && \
    $db_stop && \
    echo "export project_name=$project_name" >> /etc/apache2/envvars \
    echo "export project_root=$project_root" >> /etc/apache2/envvars \
    echo "export STATIC_ROOT=$STATIC_ROOT" >> /etc/apache2/envvars \
    ln -s /usr/local/bin/pbs-startup.sh /usr/local/bin/provision && \
    ln -s /usr/local/bin/pbs-startup.sh /usr/local/bin/provisionAndRun && \
    ln -s /usr/local/bin/pbs-startup.sh /usr/local/bin/run;

# Run CKAN and expose it by default
CMD ["startup.sh"]
EXPOSE 8080
