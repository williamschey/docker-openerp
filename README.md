# OpenERP dockerfile

## Build

sudo docker build -t jmca/openerp github.com/jmcarbo/docker-openerp

## Run

```
export DB_NAME='database'
export DB_USER='username'
export DB_PASSWORD='password'
export DB_HOST='hostname'
export DB_PORT='database_port' (5432 default)
export ADDONS_PATH='addons folder(s)'

sudo docker run -i -t -v /host/addons:/guest/addons -name=jmca_openerp jmca/openerp /bin/bash /bin/startup.sh
```
