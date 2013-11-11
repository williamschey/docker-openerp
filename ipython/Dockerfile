# Provides iPython Notebooks
FROM docker.dpaw.wa.gov.au/ubuntu
MAINTAINER Department of Parks and Wildlife <asi@dpaw.wa.gov.au>

RUN pip install -U ipython[all] pyzmq readline pexpect

ENTRYPOINT ["sh", "-c", "/usr/local/bin/ipython notebook --ip=* && bash"]
EXPOSE 8888
