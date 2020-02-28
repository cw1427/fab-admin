#!/bin/sh

# This script is a backend task schedule job to invoke the app's command.
SCRIPT_DIR=$(dirname $0)
cd $SCRIPT_DIR/..
source .profile
fabadmin ssehb >> ${SCRIPT_DIR}/../logs/sse_heartbeat.log
exit 0