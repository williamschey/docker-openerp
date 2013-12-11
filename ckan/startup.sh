#!/bin/bash
service postgresql start
service jetty start
service apache2 start
tail -f /var/log/apache2/*.log
