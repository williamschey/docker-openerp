# DPaW Joomla! website
#
# Usage: docker run dpaw/prescribed-burn-system [provisionAndRun|run|provision]
#
# Description/requirements:
#
# Sets:
#
# Exposes: 8080/pbs
#

FROM dpaw/mysql
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

# services
ENV apache2_start service apache2 start
ENV apache2_stop service apache2 stop
# project
ENV project_name dpawweb
ENV project_root /var/www/dpawweb/
ENV project_hg https://tomask:J:um:B087@hg.dec.wa.gov.au/projects/decweb/
# settings
ENV SECRET_KEY cHMYSm9hD1jBKSAZ

RUN apt-get -y install libapache2-mod-php5 mercurial php5-mysql && \
    a2dissite '*'; a2enmod rewrite expires; \
    \
    mkdir -p "$project_root" && \
    hg clone "$project_hg" -u 310 "$project_root" && \
    \
    echo "export project_root=$project_root" >> /etc/apache2/envvars; \
    echo "export project_name=$project_name" >> /etc/apache2/envvars; \
    ln -s /usr/local/bin/pbs-startup.sh /usr/local/bin/provision; \
    ln -s /usr/local/bin/pbs-startup.sh /usr/local/bin/provisionAndRun; \
    ln -s /usr/local/bin/pbs-startup.sh /usr/local/bin/run;

ADD startup.sh /usr/local/bin/startup.sh
ADD apache.conf /etc/apache2/conf.d/$project_name.conf
ADD php.ini /etc/php5/apache2/
ADD db_schema.sql $project_root/

CMD ["startup.sh"]
EXPOSE 8080
