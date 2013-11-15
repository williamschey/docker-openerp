#!/usr/bin/env python2
import subprocess, os, sys

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


def _call_install(prefix, path, repo, pip_reqs):
    print('[startup.py] Performing first-time setup of app environment')
    if not os.path.exists(prefix):
        print('[startup.py] Path "{0}" not found, creating...'.format(prefix))
        os.makedirs(prefix)
    os.chdir(prefix)
    if not os.path.exists(path):
        if (repo[:3] == 'git') or (repo[-3:] == 'git'):
            _exec(['git', 'clone', repo, path])
        else:
            _exec(['hg', 'clone', repo, path])
    _exec(['virtualenv', '.'])
    _exec([os.path.join(prefix, 'bin/pip'), 'install', '-r', pip_reqs])
    os.chdir(path)
    _exec(['service', 'postgresql', 'start'])
    _exec([os.path.join(prefix, 'bin/python'), 'manage.py', 'syncdb', '--noinput'])
    _exec([os.path.join(prefix, 'bin/python'), 'manage.py', 'migrate'])


def _call_show_bindmounts(image_name, persist_dir, mounts, port):
    print('#!/bin/bash')
    print('docker run -p '+port+':'+port+' -t -i ' + ' '.join(['-v '+
          persist_dir+mount + ':' + mount 
          for mount in mounts]) + ' '+image_name+' "$@"')


def _call_show_copymounts(image_name, persist_dir, mounts):
    print('docker run -entrypoint bash -v ' + persist_dir + ':' + 
          '/tmp/persist '+image_name+
          ' -c "' +' '.join([
          'mkdir -p ' + '/tmp/persist'+mount + '; ' +
          'cp -arvT ' + mount + ' /tmp/persist'+mount+';'
          for mount in mounts]) + '"')


def _call_manage(prefix, path, args):
    _exec(['service', 'postgresql', 'start'])
    os.chdir(path)
    if args:
        _exec([os.path.join(prefix, 'bin/python'), 'manage.py']+args)
    else:
        _exec([os.path.join(prefix, 'bin/python'), 'manage.py'])


def _call_boot(prefix, path, port):
    _exec(['service', 'postgresql', 'start'])
    os.chdir(path)
    _exec([os.path.join(prefix, 'bin/python'), 'manage.py', 'collectstatic', '--noinput'])
    _exec([os.path.join(prefix, 'bin/python'), 'manage.py', 'compress'])
    _exec([os.path.join(prefix, 'bin/python'), 'manage.py', 'run_gunicorn', '-w', '4', '-b', '0.0.0.0:'+port])


def _call_boot_shell(prefix, path, port):
    _exec(['service', 'postgresql', 'start'])
    os.chdir(path) 
    _exec([os.path.join(prefix, 'bin/python'), 'manage.py', 'collectstatic', '--noinput'])
    _exec([os.path.join(prefix, 'bin/python'), 'manage.py', 'compress'])
    server = _exec_bg([os.path.join(prefix, 'bin/python'), 'manage.py', 'run_gunicorn', '-w', '4', '-b', '0.0.0.0:'+port])   
    _exec_fg([os.path.join(prefix, 'bin/python'), 'manage.py', 'shell'])
    

if __name__ == '__main__':
    if 'container' not in os.environ:
        print('Sorry chum, it looks like you\'re not calling this script from inside a Docker container!')
        print('Perhaps you really meant to type "docker build ." instead')
        exit(-1)

    help_text = """Startup script.

Usage:
startup.py install [-d <database_url>]
startup.py show (copymounts|bindmounts) [-p <persist_dir> -i <image_name>]
startup.py manage [-d <database_url>] [<manage_arg>]...
startup.py boot [shell] [-d <database_url>] 

Options:
-h --help                   Show this screen.
-d --db=<database_url>      Use a custom database [default: postgres://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}]
-p --persist=<persist_dir>  Persistent directory (save state between runs) [default: `pwd`/persist]
-i --image=<image_name>     Name of Docker image (used to generate show statements) [default: default_base]

RUNNING: 
startup.py is specified as the entrypoint for a Docker container.

To try:
<<<<<<< local
    docker run -p 8080:8080 <image_name> boot
=======
    docker run -p {APP_PORT}:{APP_PORT} <image_name> boot
>>>>>>> other

To develop or deploy using persistent storage:
    mkdir persist
    docker run <image_name> show copymounts -i <image_name> | sh --
    docker run <image_name> show bindmounts -i <image_name> | cat > dev.sh
    chmod +x dev.sh
    ./dev.sh boot""".format(**os.environ)

    from docopt import docopt
    arguments = docopt(help_text)

    app_prefix = os.environ['APP_PREFIX']
    app_path = os.environ['APP_PATH']
    app_repo = os.environ['APP_REPO'] 
    app_pip_reqs = os.environ['APP_PIP_REQS']
    app_port = os.environ['APP_PORT']
    mounts = [x for x in (
            os.environ['DB_VOLUME'],
            os.environ['APP_VOLUME'],
            os.environ['DATA_VOLUME']
        ) if os.path.exists(x)
    ]

    os.environ['DATABASE_URL'] = arguments['--db']
    os.environ['PYTHONUNBUFFERED'] = 'x'

    image_name = arguments['--image']
    persist_dir = arguments['--persist']
    
    #print(arguments)
    #print(os.environ)

    if arguments['install']:
        _call_install(app_prefix, app_path, app_repo, app_pip_reqs)
    elif arguments['show']:
        if arguments['bindmounts']:
            _call_show_bindmounts(image_name, persist_dir, mounts, app_port)
        elif arguments['copymounts']:
            _call_show_copymounts(image_name, persist_dir, mounts)
    elif arguments['manage']:
        _call_manage(app_prefix, app_path, arguments['<manage_arg>'])
    elif arguments['boot']:
        if arguments['shell']:
            _call_boot_shell(app_prefix, app_path, app_port)
        else:
            _call_boot(app_prefix, app_path, app_port)
    else:
        print('noop')
