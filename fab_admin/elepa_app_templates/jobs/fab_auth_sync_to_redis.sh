#!/bin/sh

# This script is a backend task schedule job to invoke the app's command.
SCRIPT_DIR=$(dirname $0)
source ./.profile
fabadmin syncauth >> ${SCRIPT_DIR}/../logs/fab_auth_sync_to_redis.log
exit 0
