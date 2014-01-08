# OpenERP dockerfile

## Build

sudo docker build -t jmca/openerp github.com/jmcarbo/docker-openerp

## Run

```
sudo docker run -i -t -p 8069:8069 -e DB_NAME='database' -e DB_USER='user' -e DB_PASSWORD='password' -e DB_HOST='hosts' -e DB_PORT=5432 -e ADDONS_PATH='/addons' -v /host/addonshost:/addons -name=jmca_openerp jmca/openerp /bin/bash
```
