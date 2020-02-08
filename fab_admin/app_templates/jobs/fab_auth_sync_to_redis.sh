#!/bin/sh

# This script is a backend task schedule job to invoke the app's command.
SCRIPT_DIR=$(dirname $0)
cd /{* app_name *}
source .profile
fabadmin syncauth >> /{* app_name *}/logs/fab_auth_sync_to_redis.log
exit 0