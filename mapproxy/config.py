import os.path

from logging.config import fileConfig
from mapproxy.wsgiapp import make_wsgi_app

fileConfig(r'/opt/mapproxy/log.ini', {'here': os.path.dirname(__file__)})
application = make_wsgi_app(r'/opt/mapproxy/mapproxy.yaml')
