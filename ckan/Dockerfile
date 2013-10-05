FROM dpaw/ubuntu:12.04
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

# Install CKAN dependencies
ENV JAVA_HOME /usr/lib/jvm/java-7-oracle/
RUN apt-get install -y python-software-properties; \
add-apt-repository -y ppa:webupd8team/java; \
apt-get update; \
echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections; \
echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections; \
apt-get install -y oracle-java7-installer; \
apt-get install -y python-dev postgresql libpq-dev python-pip python-virtualenv git-core solr-jetty sudo

# Setup PostgreSQL
ENV db_host localhost # not modifiable yet
ENV db_port 5432 # not modifiable yet
ENV db_name ckan_default
ENV db_user ckan_default
ENV db_pass pass
ENV db_start /etc/init.d/postgresql start
RUN $db_start && sudo -u postgres psql -c "create user $db_user with createrole superuser password '$db_pass';"; \
sudo -u postgres createdb -O $db_user ckan_default -E utf-8 -T template0

# Setup SOLR
ENV solr_host localhost # not modifiable yet
ENV solr_port 8983
ENV solr_start /etc/init.d/jetty start
RUN mv /etc/solr/conf/schema.xml /etc/solr/conf/schema.xml.bak; \

# Setup CKAN
ENV ckan_pip -e git+https://github.com/okfn/ckan.git#egg=ckan
ENV ckan_venv /usr/lib/ckan/default
ENV ckan_etc /etc/ckan/default
RUN mkdir -p $ckan_venv; virtualenv --no-site-packages $ckan_venv; \
. $ckan_venv/bin/activate; pip install $ckan_pip; \
pip install -r $ckan_venv/src/ckan/requirements.txt
RUN . $ckan_venv/bin/activate; \
mkdir -p $ckan_etc; cd $ckan_venv/src/ckan; \
paster make-config ckan $ckan_etc/paster.ini; \
ln -s $ckan_venv/src/ckan/who.ini $ckan_etc/who.ini; \
ln -s $ckan_venv/src/ckan/ckan/config/solr/schema-2.0.xml /etc/solr/conf/schema.xml

# Write startup script
ADD ckan_startup.sh /usr/local/bin/ckan_startup.sh
RUN ckan_startup.sh init

# Run CKAN and expose it by default
CMD ["ckan_startup.sh"]
EXPOSE 5000
