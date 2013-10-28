# Mysql based on ubuntu with a default database and user.

FROM dpaw/mariadb:5.5
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

RUN apt-get -y install apache2 libapache2-mod-rpaf libapache2-mod-php5 libapache2-mod-fcgid libapache2-mod-authnz-external libapache2-mod-auth-ntlm-winbind libapache2-mod-auth-kerb
RUN apt-get -y install php5-gd php5-pgsql php5-ldap php5-memcached php5-curl php5-xmlrpc php5-intl php5-cli php5-mysql php5
RUN a2enmod authnz_ldap auth_digest auth_ntlm_winbind authnz_external rewrite expires headers

ADD startup.sh /usr/local/bin/startup.sh

ENTRYPOINT "startup.sh"
EXPOSE 80
