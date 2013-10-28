#!/bin/bash

if [ $1 == "--provision" ]; then

fi

RUN $db_start; \
    useradd $db_user; \
    sudo -u postgres psql -c \
        "CREATE USER $db_user WITH CREATEROLE SUPERUSER PASSWORD '$db_pass';";\
    sudo -u postgres createdb -O $db_user $db_name -E utf8 -T template0;\
    $db_stop;
