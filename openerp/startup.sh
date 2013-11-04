#!/bin/bash

# TODO: $db_start/$db_stop only for local DBs.

function provision()
{
    $db_start
    $db_stop
}

function run()
{
    $db_start
    $project_root/openerp-server/openerp-server --logfile=/var/log/openerp.log\
        --database="$db_name" --db-user="$db_user" --db-password="$db_pass" \
        --db-host="$db_host" --db-port="$db_port"
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
