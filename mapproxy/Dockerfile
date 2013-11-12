FROM docker.dpaw.wa.gov.au/ubuntu:12.04
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

RUN cd /opt && virtualenv --system-site-packages mapproxy
RUN /opt/mapproxy/bin/pip install MapProxy gunicorn eventlet

ADD . /opt/mapproxy

CMD ["sh", "-c", "cd /opt/mapproxy && ./bin/gunicorn -k eventlet -w 4 -b :8080 config:application"]
EXPOSE 8080
