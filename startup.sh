#!/bin/bash

# TODO: $db_start/$db_stop only for local DBs.

function provision()
{
    $DB_START
    $DB_STOP
}

function run()
{
    $DB_START
    /openerp-server/openerp-server --logfile=/var/log/openerp.log\
        --database="$DB_NAME" --db_user="$DB_USER" --db_password="$DB_PASSWORD" \
        --db_host="$DB_HOST" --db_port="$DB_PORT" --addons-path="$ADDONS_PATH"
}

SCRIPT="`basename $0`"
if [ "$SCRIPT" == "provision" ]; then
    TASK="Provision"
elif [ "$SCRIPT" == "run" ]; then
    TASK="Run"
elif [ "$SCRIPT" == "provisionAndRun" ]; then
    TASK="ProvisionAndRun"
else
    TASK=${1:-Run}
fi


if [ "${TASK^^}" == "PROVISION" ]; then
    provision
elif [ "${TASK^^}" == "RUN" ]; then
    run
elif [ "${TASK^^}" == "PROVISIONANDRUN" ]; then
    provision
    run
else
    echo "Usage: $0 [Run|Provision|ProvisionAndRun]" >&2
    exit 1
fi
