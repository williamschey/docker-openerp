'''Fabfile for automated setup of CKAN on Ubuntu 12.04 LTS
IMPORTANT: update local_settings.py with your settings,
modify private_settings_template.py and save as private_settings.py


@author Anthony Jones <mailto:anthony@gaiaresources.com.au>
@author Florian Mayer <mailto:Florian.Mayer@dpaw.wa.gov.au>

License: Apache2
Copyright: Dept Parks and Wildlife WA 2013

TODO
Run database on custom host - requires password for system user postgis
'''

import sys
import urllib2
import urllib
import json
import pprint

from fabric.api import env
from fabric.colors import red, green, yellow, cyan
from fabric.operations import run, put, sudo, prompt, local
from fabric.context_managers import cd, lcd, prefix, settings
from fabric.contrib.files import sed, upload_template, exists, is_link, uncomment, comment

from local_settings import x, ckan_api
try:
    from private_settings import z
except ImportError:
    from private_settings_template import z

#---------------------------------------------------------------------------------------------------------------------#
# main installation method
#
def prepare():
    '''MAIN PRE_INSTALL. Prepare system and db.
    '''
    prepare_system()
    setup_postgres_ckan()
    setup_postgres_datastore()
    

def install():
    '''MAIN SETUP. Run for a complete install of CKAN, SOLR running in Tomcat on custom ports/locations/hostnames. Requires fab prepare.
    '''
    #sudo('rm -rf %s' % CKAN_HOME)
    print(green('Beginning installation. Interactive prompts will be yellow.'))
    print(yellow('Please download the Java Runtime Environment "{JRE_NAME}.tar.gz" into the packages directory'.format(**x)))
    java_downloaded = prompt('Is the JRE downloaded?', default='Yep')
    if java_downloaded != 'Yep':
        print(red('Please download {JRE_NAME} into the packages directory, then re-run this script.'.format(**x)))
        sys.exit('Script aborted pending JRE download.')
    print(yellow('Provide your sudo password:'))
    #print(yellow('Enter CKAN port or keep default'))
    #HTTP_PORT = prompt('Enter CKAN port: ', default='8247')
    #print(yellow('Enter CKAN site url or keep default'))
    #CKAN_SITE_URL = prompt('Enter CKAN site url without trailing slash: ', default='http://localhost:8247')
    stop_tomcat()
    setup_directories()
    provide_dependencies()
    provide_ckan()
    install_dependencies()
    with settings(warn_only=True):
        install_ckan()
    make_apache_config()
    make_supervisor_config()
    cleanup()

#---------------------------------------------------------------------------------------------------------------------#
# installation steps
#
def prepare_system():
    '''Run once: Create db cluster, install system dependencies.
    '''
    with settings(warn_only=True):
        sudo('sudo -u postgres pg_createcluster -p {DB_PORT} 9.1 ckan --start'.format(**x))

    print(green('Installing system dependencies'))
    sudo('apt-get -y install python-dev postgresql libpq-dev python-pip python-virtualenv git-core redis-server')
    # ckanext-harvest: install either redis or rabitmq
    #sudo('apt-get install -y redis-server') 
    #sudo('apt-get install -y rabbitmq-server')
    
    # ckanext-spatial: install libxml2-dev and libxslt
    sudo('apt-get -y install libxml2-dev libxslt1-dev libgeos-c1')

def setup_directories():
    '''Creates installation destination folders CKAN and dependencies, for static and large files (e.g. for filestore plugin).
    The static folder can be outside CKAN's installation directory.
    Symlinks /media within CKAN's installation directory to the static folder.
    Sets up CKAN installation directory.
    Requires: Nothing
    Provides: CKAN_HOME, CKAN_HOME/media (and corresponding static file dir), CKAN_HOME/media/{filestore, thredds},
        CKAN_HOME/etc/default
    '''
    print(green('Creating a folder for CKAN static files underneath remote file storage mountpoint'))
    sudo('mkdir -p {CKAN_HOME}'.format(**x))
    sudo('mkdir -p {STATIC_DIR}/ckan_{HTTP_PORT}'.format(**x))
    media_folder = '{CKAN_HOME}/media'.format(**x)
    if exists(media_folder):
        sudo('rm {0}'.format(media_folder))
    sudo('ln -s {STATIC_DIR}/ckan_{HTTP_PORT} {CKAN_HOME}/media'.format(**x))
    sudo('mkdir -p {CKAN_HOME}/media/filestore'.format(**x))
    sudo('mkdir -p {CKAN_HOME}/media/thredds'.format(**x))
    sudo('chown -R www-data:www-data {STATIC_DIR}/ckan_{HTTP_PORT}'.format(**x)) # chown static dir to www-data
    sudo('chmod u+rwx {STATIC_DIR}/ckan_{HTTP_PORT}'.format(**x)) # make rwx to owner
    sudo('chown -R www-data:www-data  {CKAN_HOME}/media'.format(**x)) # chown media symlink to www-data
    sudo('chmod u+rwx {CKAN_HOME}/media'.format(**x)) # make rwx to owner

    sudo('mkdir -p {CKAN_HOME}'.format(**x))
    sudo('mkdir -p {CKAN_HOME}/lib'.format(**x))
    sudo('mkdir -p {CKAN_HOME}/etc'.format(**x))
    sudo('mkdir -p {CKAN_HOME}/etc/default'.format(**x))
    sudo('mkdir -p {DEP_DIR}'.format(**x))
    run('mkdir -p {TMP_DIR}'.format(**x))

def setup_postgres_ckan():
    '''Sets up CKAN's database. Creates a postgres user and database, will preserve either if existing.
    Requires: nothing
    Provides: A running postgres db for CKAN
    '''
    print(green('Setting up Database and db user for CKAN'))
    with settings(warn_only=True):
        sudo('sudo -u postgres createuser -p {DB_PORT} -S -D -R -P {DB_USER}'.format(**x))
        sudo('sudo -u postgres createuser -p {DB_PORT} -s {DB_ADMIN_USER}'.format(**x))
        sudo('sudo -u postgres createdb -p {DB_PORT} -O {DB_USER} {DB_NAME} -E utf-8'.format(**x))
        sudo('sudo -u postgres psql -p {DB_PORT} -d {DB_NAME} -f {POSTGIS_SCRIPT} -v ON_ERROR_ROLLBACK=on'.format(**x))
        sudo('sudo -u postgres psql -p {DB_PORT} -d {DB_NAME} -f {SRID_SCRIPT} -v ON_ERROR_ROLLBACK=on'.format(**x))
        sudo(' sudo -u postgres psql -p {DB_PORT} -d {DB_NAME} -c "ALTER TABLE spatial_ref_sys OWNER TO {DB_USER}"'.format(**x))
        sudo(' sudo -u postgres psql -p {DB_PORT} -d {DB_NAME} -c "ALTER TABLE geometry_columns OWNER TO {DB_USER}"'.format(**x))

def setup_postgres_datastore():
    '''Sets up CKAN datastore plugin's database. Creates a postgres user and database, will preserve either if existing.
    Requires: A running DB cluster on DB_HOST:DB_PORT
    Provides: A running postgres db for CKAN's datas:tore plugin
    '''
    print(green('Setting up Database and db user for CKAN plugin "datastore"'))
    print(yellow('Provide password "pass" when asked.'))
    with settings(warn_only=True):
        #sudo('sudo -u postgres createuser -S -D -R -P datastore_default')
        #sudo('sudo -u postgres createdb -O ckan_default datastore_default -E utf-8')
        sudo('sudo -u postgres createuser -p {DB_PORT} -S -D -R -P -l {DS_DB_USER}'.format(**x))
        sudo('sudo -u postgres createdb -p {DB_PORT} -O {DB_USER} {DS_DB_NAME} -E utf-8'.format(**x))
        sudo('sudo -u postgres psql -p {DB_PORT} -d {DS_DB_NAME} -f {POSTGIS_SCRIPT} -v ON_ERROR_ROLLBACK=on'.format(**x))
        sudo('sudo -u postgres psql -p {DB_PORT} -d {DS_DB_NAME} -f {SRID_SCRIPT} -v ON_ERROR_ROLLBACK=on'.format(**x))
        sudo('sudo -u postgres psql -p {DB_PORT} -d {DS_DB_NAME} -c "ALTER TABLE spatial_ref_sys OWNER TO {DB_USER}"'.format(**x))
        sudo('sudo -u postgres psql -p {DB_PORT} -d {DS_DB_NAME} -c "ALTER TABLE geometry_columns OWNER TO {DB_USER}"'.format(**x))
        # manually set permissions as per datastore/bin/set_permissions.sql -- alternatively, paster set-permissions as below
        #sudo('sudo -u postgres psql -p {DB_PORT} -d {DS_DB_NAME} -c "REVOKE CREATE ON SCHEMA public FROM PUBLIC;"'.format(**x))
        #sudo('sudo -u postgres psql -p {DB_PORT} -d {DS_DB_NAME} -c "REVOKE USAGE ON SCHEMA public FROM PUBLIC;"'.format(**x))
        #sudo('sudo -u postgres psql -p {DB_PORT} -d {DS_DB_NAME} -c "GRANT CREATE ON SCHEMA public TO {DB_USER};"'.format(**x))
        #sudo('sudo -u postgres psql -p {DB_PORT} -d {DS_DB_NAME} -c "GRANT USAGE ON SCHEMA public TO {DB_USER};"'.format(**x))
        #sudo('sudo -u postgres psql -p {DB_PORT} -d {DS_DB_NAME} -c "GRANT CREATE ON SCHEMA public TO {DS_DB_USER};"'.format(**x))
        #sudo('sudo -u postgres psql -p {DB_PORT} -d {DS_DB_NAME} -c "GRANT USAGE ON SCHEMA public TO {DS_DB_USER};"'.format(**x))
        #sudo('sudo -u postgres psql -p {DB_PORT} -d {DS_DB_NAME} -c "REVOKE CONNECT ON DATABASE {DB_NAME} FROM {DS_DB_USER};"'.format(**x))
        #sudo('sudo -u postgres psql -p {DB_PORT} -d {DS_DB_NAME} -c "GRANT CONNECT ON DATABASE {DS_DB_NAME} TO {DS_DB_USER};"'.format(**x))
        #sudo('sudo -u postgres psql -p {DB_PORT} -d {DS_DB_NAME} -c "GRANT USAGE ON SCHEMA public TO {DS_DB_USER};"'.format(**x))
        #sudo('sudo -u postgres psql -p {DB_PORT} -d {DS_DB_NAME} -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO {DS_DB_USER};"'.format(**x))
        #sudo('sudo -u postgres psql -p {DB_PORT} -d {DS_DB_NAME} -c "ALTER DEFAULT PRIVILEGES FOR USER {DB_USER} IN SCHEMA public GRANT SELECT ON TABLES TO {DS_DB_USER};"'.format(**x))

def provide_dependencies():
    '''Downloads Java dependencies (or uses local copies) and copies them into a temp directory.
    Requires: nothing
    Provides: Temp directory with script templates and downloaded archives.
    '''
    print(green('Downloading dependencies, preferring local copies.'))
    run('mkdir -p {TMP_DIR}'.format(**x)) # just in case
    # download only if needed (if remote file is newer than local file or local file doesn't exist)
    with lcd('packages'):
        local('wget -N {TOMCAT_URL}'.format(**x))
        local('wget -N {SOLR_URL}'.format(**x))
        local('wget -N {XMLLIB2_URL}'.format(**x))
    # copy all files over to temp directory    
    print(green('Copying dependencies and script templates to temporary installation folder.'))
    put('packages', x['TMP_DIR']) # templates for config files, and locally downloaded dependencies (solr, tomcat)
    print(green('Done copying install files'))

def provide_ckan():
    '''Downloads CKAN with dependencies into a virtualenv; requires fab setup_directories.
    Requires: nothing (repeats creating CKAN_HOME)
    Provides: CKAN and dependencies installed into CKAN_HOME/lib/virtualenv/
    '''
    print(green('Downloading and installing CKAN into virtualenv'))
    with cd('{CKAN_HOME}/lib'.format(**x)):
        sudo('mkdir -p virtualenv')
        sudo('virtualenv --no-site-packages virtualenv')

    with prefix('source {CKAN_HOME}/lib/virtualenv/bin/activate'.format(**x)):
        sudo('pip install -e "git+https://github.com/okfn/ckan.git#egg=ckan"')
        sudo('pip install -r {CKAN_HOME}/lib/virtualenv/src/ckan/requirements.txt'.format(**x))
        sudo('pip install -r {CKAN_HOME}/lib/virtualenv/src/ckan/dev-requirements.txt'.format(**x))
        sudo('pip install pairtree argparse') # filestore plugin
        # datastorer plugin
        sudo('pip install -e "git+https://github.com/okfn/ckanext-datastorer.git#egg=ckanext-datastorer"')
        sudo('pip install -r {CKAN_HOME}/lib/virtualenv/src/ckanext-datastorer/pip-requirements.txt'.format(**x))
        # ckanext-spatial plugin        
        sudo('pip install -e git+https://github.com/okfn/ckanext-spatial.git#egg=ckanext-spatial')
        sudo('pip install -r {CKAN_HOME}/lib/virtualenv/src/ckanext-spatial/pip-requirements.txt'.format(**x))
        

def install_dependencies():
    '''Installs system dependencies globally, and Java dependencies into CKAN's directory. Starts Tomcat.
    Requires: setup_directories(), copy()
    Provides: Java, Tomcat and SOLR installed in CKAN's DEP_DIR and running
    '''
    print(green('Installing Java dependencies'))
    with cd(x['DEP_DIR']):
        print(green('Unpacking Java dependencies JRE, SOLR, and Tomcat'))
        # It's a bit like Christmas
        sudo('tar zxf {TMP_DIR}/packages/{JRE_NAME}.tar.gz'.format(**x))
        sudo('tar zxf {TMP_DIR}/packages/{SOLR_NAME}.tgz'.format(**x))
        sudo('tar zxf {TMP_DIR}/packages/{TOMCAT_NAME}.tar.gz'.format(**x))
        sudo('tar zxf {TMP_DIR}/packages/{XMLLIB2_NAME}.tar.gz'.format(**x))
        
        # if we need libxml2-2.9.0
        #print(green('Installing libxml2'))
        #with lcd('{TMP_DIR}/packages/{XMLLIB2_NAME}.tar.gz'.format(**x)):
        #    sudo('./configure --libdir=/usr/lib/x86_64-linux-gnu')
        #    sudo('make')
        #    sudo('make install')


        print(green('Configuring SOLR'))
        # Register CKAN schema with SOLR
        sudo('cp -R {SOLR_NAME}/example {SOLR_NAME}/ckan'.format(**x))
        sudo('mv {SOLR_NAME}/ckan/solr/collection1/conf/schema.xml {SOLR_NAME}/ckan/solr/collection1/conf/schema.xml.bak'.format(**x))
        sudo('ln -s {CKAN_HOME}/lib/virtualenv/src/ckan/ckan/config/solr/schema-2.0.xml {SOLR_NAME}/ckan/solr/collection1/conf/schema.xml'.format(**x))

        print(green('Setting up SOLR to run under Tomcat'))
        # Copy SOLR .war
        sudo('cp {SOLR_NAME}/dist/{SOLR_NAME}.war {TOMCAT_NAME}/webapps'.format(**x))
        # Tomcat Java env: custom JAVA_HOME and SOLR_HOME
        upload_template('packages/setenv.sh.template', '/tmp/setenv.sh', x)
        sudo('mv /tmp/setenv.sh {DEP_DIR}/{TOMCAT_NAME}/bin/setenv.sh'.format(**x))
        sudo('cp {SOLR_NAME}/ckan/lib/ext/* {TOMCAT_NAME}/lib'.format(**x))
        # Tomcat server.xml: custom ports for listen, start, stop.
        upload_template('packages/server.xml.template', '/tmp/server.xml',x) 
        sudo('mv /tmp/server.xml {DEP_DIR}/{TOMCAT_NAME}/conf/server.xml'.format(**x))

        sudo('chown -R www-data {DEP_DIR}'.format(**x))
        start_tomcat()

    print(green('Finished installing dependencies'))

def start_tomcat():
    '''Start Tomcat application server.'''
    print(green('Starting Tomcat (& SOLR)'))
    sudo('{DEP_DIR}/{TOMCAT_NAME}/bin/startup.sh'.format(**x), pty=False, user="www-data")

def stop_tomcat():
    '''Shutdown Tomcat application server.'''
    print(green('Shutting down Tomcat (& SOLR)'))
    with settings(warn_only=True):
        sudo('{DEP_DIR}/{TOMCAT_NAME}/bin/shutdown.sh'.format(**x), pty=False, user="www-data")

def install_ckan():
    '''Installs and configures CKAN without starting it.
    Calls db and static directory setups, runs paster make-config on .ini, modifies .ini, 
    runs paster commands db init, admin add, datastore set permissions and symlinks who.ini.
    Requires: setup_directories(), setup_postgres_{ckan, datastore}()
    Provides: CKAN setup, but not running
    '''
    print(green('Begin installing ckan'))

    config = '{CKAN_HOME}/etc/default/development.ini'.format(**x)
    testconf = '{CKAN_HOME}/lib/virtualenv/src/ckan/test-core.ini'.format(**x)
    print(green('Generating CKAN config file'))
    with prefix('source {CKAN_HOME}/lib/virtualenv/bin/activate'.format(**x)):
        with cd('{CKAN_HOME}/lib/virtualenv/src/ckan'.format(**x)):
            sudo('paster make-config ckan {0}'.format(config))
    
    print(green('Writing custom settings to SOLR schema'))
    solr_schema = '{CKAN_HOME}/lib/virtualenv/src/ckan/ckan/config/solr/schema-2.0.xml'.format(**x)
    frag1 = ' type="float" indexed="true" stored="true" />'
    frag2 = '{0}\\n<field name='.format(frag1)
    sed(solr_schema, '</fields>','<field name="bbox_area"{0}"maxx"{0}"maxy"{0}"minx"{0}"miny"{1}</fields>'.format(frag2, frag1), use_sudo=True)


    print(green('Writing custom settings to CKAN config file'))
    # set solr_url
    sed(config, '#solr_url = http://127.0.0.1:8983/solr', 'solr_url = http://127.0.0.1:{TOMCAT_PORT}/{SOLR_NAME}'.format(**x), use_sudo=True)
    # enable plugins
    sed(config, 'ckan.plugins = stats text_preview recline_preview',
        'ckan.plugins = stats text_preview recline_preview {EXTRA_PLUGINS}'.format(**x),
        use_sudo=True)
    # set nofs.impl and nofs.storage_dir for filestore plugin
    #sed(config, '#ofs.impl = pairtree', 'ofs.impl = pairtree', use_sudo=True)
    uncomment(config, '#ofs.impl = pairtree', use_sudo=True)
    sed(config, '#ofs.storage_dir = /var/lib/ckan/default', 'ofs.storage_dir = {CKAN_HOME}/media/filestore'.format(**x), use_sudo=True)
    # add tracking and spatial srid after [app:main] line
    sed(config, '\\[app:main\\]', '\\[app:main\\]\\nckan.tracking_enabled = true\\nckan.spatial.srid = 4326'.format(**x), use_sudo=True) 
    # set CKAN database
    sed(config, 'sqlalchemy.url = postgresql://ckan_default:pass@localhost/ckan_default',
    'sqlalchemy.url = postgresql://{DB_USER}:{DB_PASS}@localhost:{DB_PORT}/{DB_NAME}'.format(**x), use_sudo=True)
    # datastore plugin
    sed(config, '#ckan.datastore.write_url = postgresql://ckan_default:pass@localhost/datastore_default',
    'ckan.datastore.write_url = postgresql://{DB_USER}:{DB_PASS}@localhost:{DB_PORT}/{DS_DB_NAME}'.format(**x), use_sudo=True)
    sed(config, '#ckan.datastore.read_url = postgresql://datastore_default:pass@localhost/datastore_default',
    'ckan.datastore.read_url = postgresql://{DS_DB_USER}:{DS_DB_PASS}@localhost:{DB_PORT}/{DS_DB_NAME}'.format(**x), use_sudo=True)
    # set site_url
    sed(config, 'ckan.site_url =', 'ckan.site_url = http://localhost:{HTTP_PORT}'.format(**x), use_sudo=True)
    # Front-end settings http://docs.ckan.org/en/latest/configuration.html#front-end-settings
    sed(config, 'ckan.site_title = CKAN', 'ckan.site_title = {SITE_TITLE}'.format(**x), use_sudo=True)
    sed(config, 'ckan.site_description =', 'ckan.site_description = {SITE_DESCRIPTION}'.format(**x), use_sudo=True)
    sed(config, 'ckan.site_id =', 'ckan.site_id = {SITE_ID}'.format(**x), use_sudo=True)
    sed(config, 'ckan.favicon = /images/icons/ckan.ico', 'ckan.favicon = /media/img/{FAVICON}'.format(**x), use_sudo=True)
    sed(config, 'ckan.site_logo = /base/images/ckan-logo.png', 'ckan.site_logo =\\nckan.site_intro_text = {SITE_INTRO_TEXT}\\nckan.site_about = {SITE_ABOUT}\\nckan.featured_groups = {FEATURED_GROUPS}\\nckan.featured_orgs = {FEATURED_ORGS}\\nextra_public_paths = {STATIC_DIR}/img'.format(**x), use_sudo=True)

    ## TODO any other customisations to development.ini go here
    #sed(config, 'oldstring', 'newstring', use_sudo=True)

    print(green('Writing custom settings to test config file'))
    sed(testconf, '#solr_url = http://127.0.0.1:8983/solr', 'solr_url = http://127.0.0.1:{TOMCAT_PORT}/{SOLR_NAME}'.format(**x), use_sudo=True)
    sed(testconf, 'cache_dir = %(here)s/data', 'cache_dir = /tmp/%(ckan.site_id)s/'.format(**x), use_sudo=True)
    sed(testconf, '#ckan.datastore.write_url = postgresql://ckan_default:pass@localhost/datastore_default',
    'ckan.datastore.write_url = postgresql://{DB_USER}:{DB_PASS}@localhost:{DB_PORT}/{DS_DB_NAME}'.format(**x), use_sudo=True)
    sed(testconf, '#ckan.datastore.read_url = postgresql://datastore_default:pass@localhost/datastore_default',
    'ckan.datastore.read_url = postgresql://{DS_DB_USER}:{DS_DB_PASS}@localhost:{DB_PORT}/{DS_DB_NAME}'.format(**x), use_sudo=True)

    print(green('Enabling spatial widgets'))
    dataset_search_template = '{CKAN_HOME}/lib/virtualenv/src/ckan/ckan/templates/package/search.html'.format(**x)
    # can't mix {substitution} with format() and other curly braces
    sed(dataset_search_template, '\\{% block secondary_content %\\}', 
    '\\{% block secondary_content %\\}\\n\\{% snippet "spatial/snippets/spatial_query.html", default_extent="' + x['BBOX'] + '" %\\}', use_sudo=True)

    print(green('Copying static assets: images, logos etc.'))
    put('img', '{CKAN_HOME}/media'.format(**x))
    
    print(green('Writing CKAN settings'))
    with prefix('source {CKAN_HOME}/lib/virtualenv/bin/activate'.format(**x)):
        with cd('{CKAN_HOME}/lib/virtualenv/src/ckan'.format(**x)):
            sudo('paster db init -c {CKAN_HOME}/etc/default/development.ini'.format(**x))
            sudo('paster sysadmin add admin -c {CKAN_HOME}/etc/default/development.ini'.format(**x))
            sudo('paster datastore set-permissions postgres -c {CKAN_HOME}/etc/default/development.ini'.format(**x))
        with cd('{CKAN_HOME}/etc/default'.format(**x)), settings(warn_only=True):
            sudo('ln -s {CKAN_HOME}/lib/virtualenv/src/ckan/who.ini .'.format(**x))

def make_apache_config():
    '''Provides apache.conf and apache_ckan.wsgi with custom settings. Restarts apache2.
    apache.conf -- apache config, reverse proxy for SOLR, log files
    apache_ckan.wsgi -- CKAN wsgi script using virtualenv in our custom CKAN installation directory
    Requires: copy(), install_ckan(), apache with module proxy_http enabled
    Provides: A CKAN instance running as Apache wsgi app
    '''
    print(green('Providing custom apache.conf into CKAN dir, creating symlink from global /etc/apache/conf.d'))
    upload_template('packages/apache.conf.template', '/tmp/apache.conf', x)
    sudo('mv /tmp/apache.conf {CKAN_HOME}'.format(**x))
    conf = '/etc/apache2/conf.d/{HTTP_PORT}.conf'.format(**x)
    if exists(conf) and is_link(conf):
        sudo('rm {0}'.format(conf))
    sudo('ln -s {CKAN_HOME}/apache.conf /etc/apache2/conf.d/{HTTP_PORT}.conf'.format(**x))
    
    print(green('Providing custom apache_ckan.wsgi into CKAN dir'))
    upload_template('packages/apache_ckan.wsgi.template', '/tmp/apache_ckan.wsgi', x)
    sudo('mv /tmp/apache_ckan.wsgi {CKAN_HOME}'.format(**x))

    # Set permissions, enable module proxy_http and restart apache
    print(green('Starting apache web server with proxy_http module'))
    sudo('chown -R www-data:www-data {CKAN_HOME}'.format(**x))
    sudo('a2enmod proxy_http')
    sudo('service apache2 restart')
    print(green('Success, CKAN now runs on http://localhost:{HTTP_PORT}'.format(**x)))

def make_supervisor_config():
    '''Provides a supervisord config file to let supervisor manage Tomcat.
    Requires: copy(), install_ckan()
    Provides: CKAN_HOME/supervisord.conf
    '''
    print(green('Installing supervisord.conf'))
    upload_template('packages/supervisord.conf.template', '/tmp/supervisord.conf', x)
    sudo('mv /tmp/supervisord.conf {CKAN_HOME}'.format(**x))

def cleanup():
    '''Cleans up temporary installation files by removing temp folder.
    Requires: nothing
    Provides: deletion of temp folder
    '''
    print(green('Cleaning up temporary installation files'))
    run('rm -rf {TMP_DIR}'.format(**x))


#---------------------------------------------------------------------------------------------------------------------#
# Data loading
#
def make_ckan_orgs():
    '''Create or update CKAN organizations.
    '''
    ckan_orgs = ckan_api('action/organization_list', debug=False)
    print(green('Found organizations: ' + ', '.join(ckan_orgs)))

    for i in z['orgs']:
        action = 'update' if i in ckan_orgs else 'create'
        g = ckan_api('/action/organization_{0}'.format(action), data_dict=z['orgs'][i])
        print('Organization {0}d: {1}'.format(action, i))
        #pprint.pprint(g)

def make_ckan_groups():
    '''Create or update CKAN groups.
    '''
    ckan_groups = ckan_api('action/group_list')
    print('Found groups: ' + ', '.join(ckan_groups))

    for i in z['groups']:
        action = 'update' if i in ckan_groups else 'create'
        g = ckan_api('/action/group_{0}'.format(action), data_dict=z['groups'][i])
        print(green('Group {0}d: {1}'.format(action, i)))

def make_ckan_datasets():
    '''Create or update CKAN datasets.
    '''
    ckan_datasets = ckan_api('action/package_list')
    print('Found datasets: ' + ', '.join(ckan_datasets))

    # Get details about all datasets
    #for i in ckan_datasets:
    #    ds = ckan_api('action/package_show', data_dict={'id':i})
    #    pprint.pprint(ds)

def make_ckan_users():
    '''Create or update CKAN organizations.
    '''
    ckan_users = ckan_api('action/user_list', debug=False)
    usernames = [user['name'] for user in ckan_users]
    print(green('Found users: ' + ', '.join(usernames)))

    for i in z['users']:
        if i not in usernames:
            g = ckan_api('/action/user_create', data_dict=z['users'][i])
            print('User created: {0}'.format(i))
        else:
            print('User exists, not updating: {0}'.format(i))
            
    
