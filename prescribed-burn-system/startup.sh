#!/bin/bash


function provision()
{
    $db_start
    django-admin.py deploy
    $db_stop
}

function run()
{
    $db_start
    $apache2_start
    $redis_start
    tail -f -n 0 /var/log/apache2/$project_name.error.log
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
