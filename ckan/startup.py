#!/usr/bin/env python2
'''Automated setup of CKAN on Ubuntu 12.04 LTS, Xubuntu 13

This file is modified from fabfile.py and provides both CKAN installation steps
for the docker build, as well as main method which serves as an entrypoint for Docker.

@author Adon Metcalfe <mailto:Adon.Metcalfe@dpaw.wa.gov.au>
@author Florian Mayer <mailto:Florian.Mayer@dpaw.wa.gov.au>

License: Apache2
Copyright: Dept Parks and Wildlife WA 2013
'''

import os
import subprocess
from docker_startup import DjangoStartup, with_postgresql, activate

def sed(path, old, new):
    subprocess.call(["sed", "-i", "s="+old.replace("=","\\=")+"="+new.replace("=","\\=")+"=g", path])

class CKANStartup(DjangoStartup):
    help_text = """Startup script.

Usage:
{STARTUP_SCRIPT} install [-s <site_url> -d <database_url>]
{STARTUP_SCRIPT} provision [-s <site_url>]
{STARTUP_SCRIPT} show (copymounts|bindmounts) [-p <persist_dir> -i <image_name>]
{STARTUP_SCRIPT} manage [-s <site_url>] [<manage_arg>]...
{STARTUP_SCRIPT} boot [shell] [-s <site_url>] [-u <user>]
{STARTUP_SCRIPT} shell [-c <command>]

Options:
-h --help                   Show this screen.
-d --db=<database_url>      Use a custom database [default: postgres://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}]
-s --site=<site_url>        Use a custom site url [default: http://localhost ]
-p --persist=<persist_dir>  Persistent directory (save state between runs) [default: `pwd`/persist]
-i --image=<image_name>     Name of Docker image (used to generate show statements) [default: default_base]
-u --user=<user>            Username to run the application process as [default: root]
-c --cmd=<command>          Command to execute [default: /bin/bash]

RUNNING:
{STARTUP_SCRIPT} is specified as the entrypoint for a Docker container.

To try:
    docker run -p {PORT}:{PORT} <image_name> boot

To develop or deploy using persistent storage:
    mkdir persist
    docker run <image_name> show copymounts -i <image_name> | sh --
    docker run <image_name> show bindmounts -i <image_name> | cat > dev.sh
    chmod +x dev.sh
    ./dev.sh boot"""

    def pre_entrypoint_hook(self):
        self.etc, self.filestore = (
            os.path.join(self.app_prefix, "etc"),
            os.path.join(self.app_prefix, "media", "filestore")
        )
        self.ckan_config = os.path.join(self.etc, "paster.ini")
        self.solr_schema = os.path.join(self.app_prefix, "src", "ckan", "ckan", "config", "solr", "schema-2.0.xml")
        super(CKANStartup, self).pre_entrypoint_hook()

    def _call_install(self):
        print('[{0}] Performing first-time setup of app environment'.format(
            os.environ['STARTUP_SCRIPT']))

        # create the directory
        if not os.path.exists(self.app_prefix):
            print('[{0}] Path "{1}" not found, creating...'.format(
                os.environ['STARTUP_SCRIPT'], self.app_prefix))
            os.makedirs(self.app_prefix)

        # install virtualenv
        os.chdir(self.app_prefix)
        self._exec_fg(['virtualenv', '.'])
        activate(self.app_prefix)

        self._exec_fg(['pip', 'install', '--editable', self.app_repo])
        self._exec_fg(['pip', 'install', '-r', os.path.join(self.app_prefix, "src", "ckan", 'requirements.txt')])

        os.chdir(self.app_prefix)

        # deploy
        def deploy(self):
            os.makedirs(self.etc)
            os.makedirs(self.filestore)
            self._exec_fg(["pip", "install", "pairtree", "argparse", "paste"])
            self._exec_fg(["pip", "install", "--editable", "git+https://github.com/okfn/ckanext-datastorer.git#egg=ckanext-datastorer"])
            self._exec_fg(["pip", "install", "-r", os.path.join(self.app_prefix, "src", "ckanext-datastorer", "pip-requirements.txt")])
            self._exec_fg(["pip", "install", "--editable", "git+https://github.com/okfn/ckanext-spatial.git#egg=ckanext-spatial"])
            self._exec_fg(["pip", "install", "-r", os.path.join(self.app_prefix, "src", "ckanext-spatial", "pip-requirements.txt")])
            sed("/etc/default/jetty", ".*NO_START=.*", "NO_START=0")
            sed("/etc/default/jetty", ".*JETTY_PORT=.*", "JETTY_PORT={SOLR_PORT}".format(**os.environ))
            frag1 = ' type="float" indexed="true" stored="true" />'
            frag2 = '{0}\\n<field name='.format(frag1)
            sed(self.solr_schema, '</fields>','<field name="bbox_area"{0}"maxx"{0}"maxy"{0}"minx"{0}"miny"{1}</fields>'.format(frag2, frag1))
            self._exec_fg(["ln", "-sf", self.solr_schema, "/etc/solr/conf/schema.xml"])
            self._exec_fg(["paster", "make-config", "ckan", self.ckan_config])

        with_postgresql(deploy)(self)

    @with_postgresql
    def _call_provision(self, db_url):
        db_url = db_url.replace("postgres:", "postgresql:")
        ckan_dburl = "postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}".format(**os.environ)
        dswrite_dburl = "postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{DS_PGDATABASE}".format(**os.environ)
        dsread_dburl = "postgresql://{DS_PGUSER}:{DS_PGPASSWORD}@{PGHOST}:{PGPORT}/{DS_PGDATABASE}".format(**os.environ)
        sed(self.ckan_config, '#solr_url = .*$', 'solr_url = http://{SOLR_HOST}:{SOLR_PORT}/solr'.format(**os.environ))
        # enable a handful of plugins
        my_plugins = 'stats text_preview recline_preview pdf_preview resource_proxy datastore'+\
        ' spatial_metadata spatial_query geojson_preview wms_preview'
        sed(self.ckan_config, 'ckan.plugins =.*$', 'ckan.plugins = ' + my_plugins)
        # set nofs.impl and nofs.storage_dir for filestore plugin
        sed(self.ckan_config, '#ofs.impl = pairtree', 'ofs.impl = pairtree')
        sed(self.ckan_config, '#ofs.storage_dir = .*$', 'ofs.storage_dir = ' + self.filestore)
        # add tracking and spatial srid after [app:main] line, (linebreaks are \\n, angled brackets are \\[ and \\])
        sed(self.ckan_config, '\\[app:main\\]', '\\[app:main\\]\\nckan.tracking_enabled = true\\nckan.spatial.srid = 4326') 
        # set CKAN database -- env variable uses Django convention "postgres:"
        sed(self.ckan_config, 'sqlalchemy.url = .*$', 'sqlalchemy.url = ' + ckan_dburl)
        # datastore plugin
        sed(self.ckan_config, '#ckan.datastore.write_url = .*$', 'ckan.datastore.write_url = ' + dswrite_dburl)
        sed(self.ckan_config, '#ckan.datastore.read_url = .*$', 'ckan.datastore.read_url = ' + dsread_dburl)
        # set site_url
        sed(self.ckan_config, 'ckan.site_url =', 'ckan.site_url = ' + self.arguments["--site"])

CKANStartup(app_repo="git+https://github.com/okfn/ckan.git#egg=ckan")

"""
def configure(arguments):
    '''Installs and configures CKAN without starting it.
    Calls db and static directory setups, runs paster make-config on .ini, modifies .ini, 
    runs paster commands db init, admin add, datastore set permissions and symlinks who.ini.
    Requires: setup_directories(), setup_postgres_{ckan, datastore}()
    Provides: CKAN setup, but not running
    '''
    print(green('Begin configuring ckan'))
    config = '{APP_PREFIX}/ckan_home/etc/default/paster.ini'.format(**os.environ) # development.ini renamed
    virtualbin = '{APP_PREFIX}/ckan_home/lib/virtualenv/bin'.format(**os.environ) # virtualenv/bin

    # setup Jetty

    print(green('Writing custom settings to CKAN config file'))
    # set solr_url
    sed(config, '#solr_url = .*$', 'solr_url = http://{SOLR_HOST}:{SOLR_PORT}/solr'.format(**os.environ))
    # enable a handful of plugins
    my_plugins = 'stats text_preview recline_preview pdf_preview resource_proxy datastore'+\
    ' spatial_metadata spatial_query geojson_preview wms_preview'
    sed(config, 'ckan.plugins =.*$', 'ckan.plugins = ' + my_plugins)
    # set nofs.impl and nofs.storage_dir for filestore plugin
    sed(config, '#ofs.impl = pairtree', 'ofs.impl = pairtree')
    sed(config, '#ofs.storage_dir = .*$', 'ofs.storage_dir = {APP_PREFIX}/ckan_home/media/filestore'.format(**os.environ))
    # add tracking and spatial srid after [app:main] line, (linebreaks are \\n, angled brackets are \\[ and \\])
    sed(config, '\\[app:main\\]', '\\[app:main\\]\\nckan.tracking_enabled = true\\nckan.spatial.srid = 4326') 
    # set CKAN database -- env variable uses Django convention "postgres:"
    sed(config, 'sqlalchemy.url = .*$', 
        #'sqlalchemy.url = {0}'.format(arguments["--db"].replace("postgres:", "postgresql:")))
        'sqlalchemy.url = postgresql://{PGUSER}:{PGPASSWORD}@localhost:{PGPORT}/{PGDATABASE}'.format(**os.environ))
    # datastore plugin
    sed(config, '#ckan.datastore.write_url = .*$',
        #'ckan.datastore.write_url = {0}'.format(arguments["--dswrite"].replace("postgres:", "postgresql:")))
        'ckan.datastore.write_url = postgresql://{PGUSER}:{PGPASSWORD}@localhost:{PGPORT}/{PGDATASTORE}'.format(**os.environ))
    sed(config, '#ckan.datastore.read_url = .*$',
        #'ckan.datastore.read_url = {0}'.format(arguments["--dsread"].replace("postgres:", "postgresql:")))
        'ckan.datastore.read_url = postgresql://{DSUSER}:{DSPASSWORD}@localhost:{PGPORT}/{PGDATASTORE}'.format(**os.environ))
    # set site_url
    sed(config, 'ckan.site_url =', 'ckan.site_url = ' + arguments["--url"])

    print(green('Customising CKAN frontend settings: logo, favicon, title etc. from local_settings.py'))
    # Front-end settings http://docs.ckan.org/en/latest/configuration.html#front-end-settings
    subprocess.call(["rsync", "-Pavvr", "{APP_PATH}/img/".format(**os.environ), 
        '{APP_PREFIX}/ckan_home/media/img/'.format(**os.environ)], shell=True)
    sed(config, 'ckan.site_title = .*$', 'ckan.site_title = {SITE_TITLE}'.format(**x))
    sed(config, 'ckan.site_description =', 'ckan.site_description = {SITE_DESCRIPTION}'.format(**x))
    sed(config, 'ckan.site_id =', 'ckan.site_id = {SITE_ID}'.format(**x))
    sed(config, 'ckan.favicon = .*$', 'ckan.favicon = /media/img/{FAVICON}'.format(**x))
    sed(config, 'ckan.site_logo = .*$', 
    'ckan.site_logo =\\nckan.site_intro_text = {SITE_INTRO_TEXT}\\nckan.site_about = {SITE_ABOUT}\\nckan.featured_groups = {FEATURED_GROUPS}\\nckan.featured_orgs = {FEATURED_ORGS}\\nextra_public_paths = {STATIC_DIR}/img'.format(**x))
    
    print(green('Enabling spatial widgets'))
    dataset_search_template = '{APP_PREFIX}/ckan_home/lib/virtualenv/src/ckan/ckan/templates/package/search.html'.format(**os.environ)
    # can't mix {substitution} with format() and other curly braces, workaround '' + var + ''
    sed(dataset_search_template, '\\{% block secondary_content %\\}', 
    '\\{% block secondary_content %\\}\\n\\{% snippet "spatial/snippets/spatial_query.html", default_extent="' + x['BBOX'] + '" %\\}')

    print(green('Writing CKAN settings'))
    subprocess.call(["/etc/init.d/jetty", "start"])
    subprocess.call(["/etc/init.d/postgresql", "start"])
    os.chdir('{APP_PREFIX}/ckan_home/lib/virtualenv/src/ckan'.format(**os.environ))
    subprocess.call(virtualbin + '/paster db init -c {APP_PREFIX}/ckan_home/etc/default/paster.ini'.format(**os.environ), shell=True)
    subprocess.call(virtualbin + 
        '/paster sysadmin add admin -c {APP_PREFIX}/ckan_home/etc/default/paster.ini'.format(**os.environ), shell=True)
    subprocess.call(virtualbin + 
        '/paster datastore set-permissions postgres -c {APP_PREFIX}/ckan_home/etc/default/paster.ini'.format(**os.environ), shell=True)
    os.chdir('{APP_PREFIX}/ckan_home/etc/default'.format(**os.environ))
    subprocess.call('ln -sf {APP_PREFIX}/ckan_home/lib/virtualenv/src/ckan/who.ini .'.format(**os.environ), shell=True)
    
    print(green('CKAN config finished successfully!'))

#---------------------------------------------------------------------------------------------------------------------#
# Docker build: main method (calls Fabric build steps)
#
if __name__ == '__main__':
    if 'container' not in os.environ:
        print('Sorry chum, it looks like you\'re not calling this script from inside a Docker container!')
        print('Perhaps you really meant to type "docker build ." instead')
        exit(-1)

    from docopt import docopt
    arguments = docopt(help_text)
    print(arguments)

    app_prefix = os.environ['APP_PREFIX']
    mounts = [os.environ['DB_VOLUME'], os.environ['APP_VOLUME'],os.environ['DATA_VOLUME']]

    if arguments['install']:
        install(arguments)
    elif arguments['configure']:
        configure(arguments)
    elif arguments['show']:
        if arguments['bindmounts']:
            print('docker run ' + 
                ' '.join(['-v '+ arguments['--persist']+mount + ':' + mount for mount in mounts]) + ' ' +arguments['--image'])
        elif arguments['copymounts']:
            print('docker run -entrypoint bash -v ' + arguments['--persist'] + ':' + '/tmp/persist '+arguments['--image']+
                ' -c "' +'\n'.join(['mkdir -p ' + '/tmp/persist'+mount + '; ' + 'cp -arvT ' + mount + ' /tmp/persist'+ mount
                for mount in mounts]) + '"' )
    else:
        subprocess.call(["/etc/init.d/jetty", "start"])
        subprocess.call(["/etc/init.d/postgresql", "start"])
        virtualbin = '{APP_PREFIX}/ckan_home/lib/virtualenv/bin'.format(**os.environ) # virtualenv/bin
        config = '{APP_PREFIX}/ckan_home/etc/default/paster.ini'.format(**os.environ) # development.ini renamed
        subprocess.call(virtualbin + "/paster serve " + config)

"""
