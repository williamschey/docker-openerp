FROM dpaw/postgis:2.1
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

# Setup PostgreSQL
ENV db_host localhost # not modifiable yet
ENV db_port 5432 # not modifiable yet
ENV db_name pbs_8204
ENV db_user pbs
ENV db_pass pbs
ENV db_start /etc/init.d/postgresql start
RUN $db_start && sudo -u postgres psql -c "create user $db_user with createrole superuser password '$db_pass';"; \
sudo -u postgres createdb -O $db_user $db_name -E utf-8
sudo -u postgres psql -c "create extension postgis" $db_name

# Setup Apache

# Setup PBS
ENV pbs_pip https://bitbucket.org/dpaw/prescribed-burn-system/get/OCE-3_Publish-PBS.zip
ENV pbs_venv /var/www/pbs_8204/
RUN mkdir -p $pbs_venv; virtualenv --no-site-packages $pbs_venv; \
. $pbs_venv/bin/activate; pip install $pbs_pip; \
ln -s $pbs_venv/apache.conf $ckan_etc/who.ini; \

# Run CKAN and expose it by default
CMD ["ckan_startup.sh"]
EXPOSE 8080     # expose pbs via apache
