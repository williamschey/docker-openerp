#!/usr/bin/env python2
'''Automated startup of R studio server


@author Florian Mayer <mailto:Florian.Mayer@dpaw.wa.gov.au>

License: Apache2
Copyright: Dept Parks and Wildlife WA 2013

'''
import os
import sys
import urllib2
import urllib
import json
import pprint
import subprocess, os

from fabric.colors import red, green, yellow, cyan

from local_settings import x # custom settings

# Redefine sed to make it usable during docker install, use instead of fabric's sed
def sed(path, old, new):
    subprocess.call(["sed", "-i", "s="+old.replace("=","\\=")+"="+new.replace("=","\\=")+"=g", path])

# Force unbuffered output
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

#---------------------------------------------------------------------------------------------------------------------#
# Docker build: main method
#
if __name__ == '__main__':
    if 'container' not in os.environ:
        print('Sorry chum, it looks like you\'re not calling this script from inside a Docker container!')
        print('Perhaps you really meant to type "docker build ." instead')
        exit(-1)

    help_text = """Startup script.

Usage:
startup.py show (copymounts|bindmounts) [-p <persist_dir> -i <image_name>]
startup.py

Options:
-h --help                   Show this screen.
-p --persist=<persist_dir>  Persistent directory (save state between runs) [default: `pwd`/persist]
-i --image=<image_name>     Name of Docker image (used to generate show statements) [default: default_base]
-u --url=<site_url>         URL CKAN is published on [default: http://localhost:5000]

RUNNING: 
startup.py is specified as the entrypoint for a Docker container.

To try:
    docker run <image_name> 

To develop or deploy using persistent storage:
    docker run <image_name> show copymounts -i <image_name> | sh --
    docker run <image_name> show bindmounts -i <image_name> | cat > dev.sh
    chmod +x dev.sh
    ./dev.sh
    format""".format(**os.environ)

    from docopt import docopt
    arguments = docopt(help_text)
    print(arguments)

    app_prefix = os.environ['APP_PREFIX']
    mounts = [os.environ['DB_VOLUME'], os.environ['APP_VOLUME'],os.environ['DATA_VOLUME']]
    os.environ['DATABASE_URL'] = arguments['--db'][0]

    if arguments['show']:
        if arguments['bindmounts']:
            print('docker run ' + 
                ' '.join(['-v '+ arguments['--persist']+mount + ':' + mount for mount in mounts]) + ' ' +arguments['--image'])
        elif arguments['copymounts']:
            print('docker run -entrypoint bash -v ' + arguments['--persist'] + ':' + '/tmp/persist '+arguments['--image']+
                ' -c "' +'\n'.join(['mkdir -p ' + '/tmp/persist'+mount + '; ' + 'cp -arvT ' + mount + ' /tmp/persist'+ mount
                for mount in mounts]) + '"' )
    else:
        subprocess.call(["rstudio-server", "restart"])
