FROM dpaw/ubuntu
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

RUN apt-get install -y python-pip python-imaging python-yaml python-dev libproj0 libgeos-dev python-lxml libgdal-dev && pip install virtualenv
RUN cd /opt && virtualenv --system-site-packages mapproxy
RUN /opt/mapproxy/bin/pip install MapProxy gunicorn eventlet

ADD . /opt/mapproxy

CMD ["sh", "-c", "cd /opt/mapproxy && ./bin/gunicorn -k eventlet -w 4 -b :8080 config:application"]
EXPOSE 8080
