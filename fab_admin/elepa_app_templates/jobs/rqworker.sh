#!/bin/sh
# This script is going to rotate the uwsgi log daily.
SCRIPT_DIR=$(dirname $0)
source ./.profile
flask rq worker
