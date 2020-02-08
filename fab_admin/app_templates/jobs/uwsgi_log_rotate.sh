#!/bin/sh
# This script is going to rotate the uwsgi log daily.
SCRIPT_DIR=$(dirname $0)
cd /{* app_name *}/logs
target_date=`date -d "-24:00" +%Y%m%d`
mv uwsgi-log uwsgi-log-${target_date}
touch .touchforlogrotate
exit 0