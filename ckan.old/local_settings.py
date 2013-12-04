
import urllib2
import urllib
import json
import pprint
#---------------------------------------------------------------------------------------------------------------------#
# Defaults
#
# x: A dictionary of defaults
# ''.format(**x) your commands using the {KEY_NAMES} for declarative string substitution
x = {

#---------------------------------------------------------------------------------------------------------------------#
## deployment settings - modify as required
'TMP_DIR': '/tmp/ckan_install', # a temp folder for install files, will be emptied after installation
'STATIC_DIR': '/mnt/remote/static', # destination for large/static files, ideally a mounted fileshare
'HTTP_PORT': '8247', # the port to run CKAN under (as string!) - after installation, you can access CKAN under http://localhost:HTTP_PORT
'DB_HOST': 'pgsql-001', # (pgsql-001 is an alias in /etc/hosts pointing to the corresponding db server)
'DB_PORT': '5456', # pre-allocated by IT ops for DPaW
'DB_NAME': 'ckan_default',
'DB_USER': 'ckan_default',
'DB_PASS': 'pass',
'DB_ADMIN_USER': 'ckan_admin',
'DB_ADMIN_PASS': 'narwhal_bacon',
'DS_DB_NAME': 'datastore_default',
'DS_DB_USER': 'datastore_default',
'DS_DB_PASS': 'pass',
'CKAN_BASE': '/var/www/ckan', # the installation base directory prefix
'POSTGIS_SCRIPT': '/usr/share/postgresql/9.3/contrib/postgis-2.0/postgis.sql', # depends on your postgres and postgis version
'SRID_SCRIPT': '/usr/share/postgresql/9.3/contrib/postgis-2.0/spatial_ref_sys.sql', # same here

#---------------------------------------------------------------------------------------------------------------------#
## Dependencies - update as required
'SOLR_URL':  'http://mirror.overthewire.com.au/pub/apache/lucene/solr/4.5.0/solr-4.5.0.tgz', # a download mirror for SOLR
'SOLR_NAME':  'solr-4.5.0', # the SOLR name and version
'TOMCAT_URL':  'http://mirror.ventraip.net.au/apache/tomcat/tomcat-7/v7.0.42/bin/apache-tomcat-7.0.42.tar.gz', # a download mirror for TOMCAT
'TOMCAT_NAME':  'apache-tomcat-7.0.42', # the tomcat name and version
'JRE_NAME': 'server-jre-7u40-linux-x64', # the JRE name and version
'JDK_NAME': 'jdk1.7.0_40',
'XMLLIB2_URL': 'http://xmlsoft.org/sources/libxml2-2.9.0.tar.gz',
'XMLLIB2_NAME':'libxml2-2.9.0',

#---------------------------------------------------------------------------------------------------------------------#
# Config file customisations
# http://docs.ckan.org/en/latest/configuration.html#front-end-settings
'SITE_ID':'data.dpaw.wa.gov.au',
'SITE_TITLE': 'DPaW Data',
'SITE_DESCRIPTION': 'Biodiversity Conservation Data',
'SITE_INTRO_TEXT': 'Welcome to the DPaW data catalog. Discover and access datasets and products relevant to biodiversity conservation.',
'SITE_LOGO':'logo-dpaw.gif',
'FAVICON':'favicon.ico',
'SITE_ABOUT':'[Usage statistics](/stats) | [layout test](/testing/primer) | [HTML5 compliance](http://html5test.com).',
'FEATURED_GROUPS': 'gorgon-dredging gorgon-turtles',
'FEATURED_ORGS': 'dpaw-marine',
'BBOX': '[[-35, 115], [-10, 130]]', # your initial bounding box for dataset search page map widget -- defaults to WA
'EXTRA_PLUGINS': 'pdf_preview resource_proxy datastore spatial_metadata spatial_query geojson_preview wms_preview',
}

# variables calculated from other keys of x
x['CKAN_HOME'] = '{CKAN_BASE}_{HTTP_PORT}'.format(**x) # the installation base directory - /var/www/ckan_HTTP_PORT
x['DEP_DIR'] = '{CKAN_HOME}/opt'.format(**x) # a subfolder for CKAN dependencies
x['CKAN_SITE_URL'] = 'http://localhost:{HTTP_PORT}'.format(**x), # the CKAN site_url, required for some plugins

# required variables for template substitution
x['JAVA_HOME'] = '{DEP_DIR}/{JDK_NAME}'.format(**x)
x['SOLR_HOME'] = '{DEP_DIR}/{SOLR_NAME}/ckan/solr'.format(**x)
x['TOMCAT_PORT_PREFIX'] = x['HTTP_PORT'][1:] # if HTTP_PORT is 8247, TOMCAT_PORT_PREFIX should be 247
x['TOMCAT_PORT'] = '{0}1'.format(x['TOMCAT_PORT_PREFIX']) # if HTTP_PORT is 8247, TOMCAT_PORT should be 2471


#-----------------------------------------------------------------------------#
# Utility functions
#
def ckan_api(action_string, data_dict={}, debug=False):
    '''Sends an API request to the API url plus your url path with your data.
    
    Positional arguments:
    action_string -- Additional url path (e.g. 'action/group_list')

    Keyword adguments:
    data_dict -- A python dict of request parameters, default: {}
    debug -- Toogle debug output for your requests
    
    Returns
    The value of the reponse key "result" if the request was successful.
    '''
    url = '{0}{1}'.format(x['url'], action_string)
    data = urllib.quote(json.dumps(data_dict))
    if debug:
        print('[debug] GET {0} with data {1}'.format(url, data_dict))
    request = urllib2.Request(url)
    request.add_header('Authorization', x['key'])
    response = urllib2.urlopen(request, data)
    if debug:
        print('[debug] ' + str(response.code))
    assert response.code == 200
    response_dict = json.loads(response.read())    
    if debug:
        print(response_dict['help'])
    assert response_dict['success'] is True
    return response_dict['result']
