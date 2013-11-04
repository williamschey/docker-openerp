# Confluence java app
#
# Usage: docker run dpaw/confluence [provisionAndRun|run|provision]
#
# Description/requirements:
#
# Sets:
#
# Exposes: 8080/confluence
#

FROM dpaw_ubuntu:12.04
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

ENV project_name confluence
ENV project_root /var/www/
ENV confluence_url http://www.atlassian.com/software/confluence/downloads/binary/atlassian-confluence-5.3.1-x64.bin
ENV ATTACHMENTS_DIR /mnt/remote/static/confluence/attachments/
ENV confluence_start $project_root/bin/start-confluence.sh -fg

ADD response.varfile $project_root/
ADD confluence_8222/ $project_root/confluence_8222
ADD confluence_8222.home/ $project_root/confluence_8222.home
ADD startup.sh /usr/local/bin/startup.sh

RUN apt-get -y install wget; \
    cd $project_root; \
    wget $confluence_url;
#    bash atlassian-confluence-*.bin -q -varfile $project_root/response.varfile
RUN ln -s /usr/local/bin/pbs-startup.sh /usr/local/bin/provision; \
    ln -s /usr/local/bin/pbs-startup.sh /usr/local/bin/provisionAndRun; \
    ln -s /usr/local/bin/pbs-startup.sh /usr/local/bin/run;

# Run confluence and expose it by default
CMD ["startup.sh"]
EXPOSE 8090
