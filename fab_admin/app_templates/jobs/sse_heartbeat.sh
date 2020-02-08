#!/bin/sh

# This script is a backend task schedule job to invoke the app's command.
SCRIPT_DIR=$(dirname $0)
cd /bas
source .profile
fabadmin ssehb >> /{* app_name *}/logs/sse_heartbeat.log
exit 0