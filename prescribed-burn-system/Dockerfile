# Prescribed burn system django app
#
# Usage: docker run dpaw/prescribed-burn-system [provisionAndRun|run|provision]
#
# Description: Clones and installs django-prescribed-burn-system into
#              $project_root in development mode (along with all dependencies).
#
# Sets: $apache2_start, $redis_start, $project_name, $project_root,
#       $project_logs, $project_pip, $STATIC_ROOT, $MEDIA_ROOT, $SECRET_KEY,
#       $DJANGO_SETTINGS_MODULE
#
# Exposes: 8080/pbs
#

FROM dpaw_ubuntu:12.04
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

# Setup PBS
ENV apache2_start apachectl start
ENV redis_start service redis-server start
# project settings
ENV project_name pbs
ENV project_root /var/www/django_project/
ENV project_logs /var/log/django/
ENV project_pip hg+https://hg.dec.wa.gov.au/projects/prescribed-burn-system@2300
# django settings
ENV STATIC_ROOT /var/www/django_project_static/
ENV MEDIA_ROOT /var/www/django_project_media/
ENV SECRET_KEY 7e8964cebd5a2c8f3cb402337a05c8b5c92cd266c252bd8c1ca003c41a3443f4
ENV DJANGO_SETTINGS_MODULE pbs.settings

# install dependencies, pbs, startup script
RUN a2dissite '*'; \
    mkdir -p "$project_logs" && chown -R :www-data "$project_logs" && \
    chmod -R g+ws "$project_logs" && \
    mkdir -p "$MEDIA_ROOT" && \
    mkdir -p "$project_root" && cd "$project_root"
RUN pip install -M --index-url 'https://hg.dec.wa.gov.au/pypi' \
        --extra-index-url 'http://pypi.python.org/pypi' \
        -e "$project_pip#egg=$project_name"

ADD startup.sh /usr/local/bin/startup.sh
ADD apache.conf /etc/apache2/conf.d/django_project.conf

CMD ["startup.sh"]
EXPOSE 8080
