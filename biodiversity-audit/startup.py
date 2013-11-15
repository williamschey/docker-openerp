#!/usr/bin/env python2

# TODO: this doesn't look very nice/simple/elegant, :( FIXME/FIXME :)
try:
    from docker_startup import DjangoStartup
except ImportError:
    import os
    os.system('pip install '
              'hg+https://bitbucket.org/dpaw/docker-startup'
              '#egg=docker-startup')
    from docker_startup import DjangoStartup

DjangoStartup(app_repo="https://bitbucket.org/dpaw/biodiversity-audit.git")
