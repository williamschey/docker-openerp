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

#FROM dpaw/mysql
FROM fa08a30ffa44
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

# dependencies
RUN apt-get -y install libapache2-mod-php5 mercurial php5-mysql && \
    a2dissite '*'; a2enmod rewrite expires

ENV apache2_start service apache2 start
ENV apache2_stop service apache2 stop

# Setup DPaW website
ENV project_name dpawweb
ENV project_root /var/www/dpawweb/
ENV project_hg https://hg.dec.wa.gov.au/projects/decweb/
ENV SECRET_KEY cHMYSm9hD1jBKSAZ

ADD startup.sh /usr/local/bin/startup.sh
ADD apache.conf /etc/apache2/conf.d/$project_name.conf

# TODO: static environment variables set during the image build and environment
# variables changeable during runtime!!!!

RUN mkdir -p "$project_root" && \
    hg clone "$project_hg" -u 309 "$project_root" && \
    echo "export project_root=$project_root" >> /etc/apache2/envvars; \
    echo "export project_name=$project_name" >> /etc/apache2/envvars; \
    echo "export db_name=$db_name" >> /etc/apache2/envvars; \
    echo "export db_host=$db_host" >> /etc/apache2/envvars; \
    echo "export db_user=$db_user" >> /etc/apache2/envvars; \
    echo "export db_pass=$db_pass" >> /etc/apache2/envvars; \
    echo "export SECRET_KEY=$SECRET_KEY" >> /etc/apache2/envvars; \
    ln -s /usr/local/bin/pbs-startup.sh /usr/local/bin/provision; \
    ln -s /usr/local/bin/pbs-startup.sh /usr/local/bin/provisionAndRun; \
    ln -s /usr/local/bin/pbs-startup.sh /usr/local/bin/run;

CMD ["startup.sh"]
EXPOSE 8080
