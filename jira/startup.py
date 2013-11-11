#!/usr/bin/env python2
import subprocess, os, sys, time

# Force unbuffered output
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)


def _exec(argv):
    print('[startup.py] Running "{0}"...'.format(' '.join(argv)))
    proc = subprocess.Popen(argv, stdout=subprocess.PIPE)
    for line in proc.stdout.readlines():
        print(line)
    proc.wait()
    if (proc.returncode != 0):
        print('[startup.py] "{0}" returned {1}, exiting!'.format(' '.join(argv), proc.returncode))
        exit(proc.returncode)


def _exec_bg(argv):
    print('[startup.py] Starting background process "{0}"...'.format(' '.join(argv)))
    proc = subprocess.Popen(argv, stdout=subprocess.PIPE)
    return proc


def _exec_fg(argv):
    print('[startup.py] Starting foreground process "{0}"...'.format(' '.join(argv)))
    os.system(' '.join(argv))


def _call_show_bindmounts(image_name, persist_dir, mounts):
    print('#!/bin/bash')
    print('docker run -t -i ' + ' '.join(['-v '+
          persist_dir+mount + ':' + mount 
          for mount in mounts]) + ' '+image_name+' "$@"')


def _call_show_copymounts(image_name, persist_dir, mounts):
    print('docker run -entrypoint bash -v ' + persist_dir + ':' + 
          '/tmp/persist '+image_name+
          ' -c "' +' '.join([
          'mkdir -p ' + '/tmp/persist'+mount + '; ' +
          'cp -arvT ' + mount + ' /tmp/persist'+mount+';'
          for mount in mounts]) + '"')


def _call_boot(path):
    _exec(['service', 'postgresql', 'start'])
    _exec([os.path.join(path, "bin", "startup.sh")])
    logfile = os.path.join(os.environ["APP_VOLUME"], "log", "atlassian-jira.log")
    while not os.path.exists(logfile):
        print("waiting...")
        time.sleep(0.5)
    _exec_fg(['tail', "-f", logfile])

def _call_boot_shell(path):
    _exec(['service', 'postgresql', 'start'])
    _exec([os.path.join(path, "bin", "startup.sh")])
    _exec_fg(['bash'])
    

if __name__ == '__main__':
    if 'container' not in os.environ:
        print('Sorry chum, it looks like you\'re not calling this script from inside a Docker container!')
        print('Perhaps you really meant to type "docker build ." instead')
        exit(-1)

    help_text = """Startup script.

Usage:
startup.py show (copymounts|bindmounts) [-p <persist_dir> -i <image_name>]
startup.py boot [shell] [-d <database_url>] 

Options:
-h --help                   Show this screen.
-p --persist=<persist_dir>  Persistent directory (save state between runs) [default: `pwd`/persist]
-i --image=<image_name>     Name of Docker image (used to generate show statements) [default: default_base]

RUNNING: 
startup.py is specified as the entrypoint for a Docker container.

To try:
<<<<<<< local
    docker run -p 8080:8080 <image_name> boot
=======
    docker run -p APP_PORT:APP_PORT <image_name> boot
>>>>>>> other

To develop or deploy using persistent storage:
    mkdir persist
    docker run <image_name> show copymounts -i <image_name> | sh --
    docker run <image_name> show bindmounts -i <image_name> | cat > dev.sh
    chmod +x dev.sh
    ./dev.sh boot""".format(**os.environ)

    from docopt import docopt
    arguments = docopt(help_text)

    mounts = [x for x in (
            os.environ['DB_VOLUME'],
            os.environ['APP_VOLUME'],
        ) if os.path.exists(x)
    ]

    os.environ['PYTHONUNBUFFERED'] = 'x'

    image_name = arguments['--image']
    persist_dir = arguments['--persist']
    
    #print(arguments)
    #print(os.environ)

    if arguments['show']:
        if arguments['bindmounts']:
            _call_show_bindmounts(image_name, persist_dir, mounts)
        elif arguments['copymounts']:
            _call_show_copymounts(image_name, persist_dir, mounts)
    elif arguments['boot']:
        if arguments['shell']:
            _call_boot_shell(os.environ["APP_FILES"])
        else:
            _call_boot(os.environ["APP_FILES"])
    else:
        print('noop')
