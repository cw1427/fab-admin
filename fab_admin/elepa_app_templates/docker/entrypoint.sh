#!/bin/sh

# Explicitly add installed Python packages and uWSGI Python packages to PYTHONPATH
# Otherwise uWSGI can't import Flask
export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/site-packages:/usr/lib/python2.7/site-packages

# If GOSU_CHOWN environment variable set, recursively chown all specified directories
# to match the user:group set in GOSU_USER environment variable.
if [ -n "$GOSU_CHOWN" ]; then
    for DIR in $GOSU_CHOWN
    do
        chown -R $GOSU_USER $DIR
    done
fi

#----read db password from current path
if [ -f ${DB_PWD_FILE} ]; then
    export DB_PWD=$(cat ${DB_PWD_FILE})
fi


# set all sh file in jobs folder executable property
chmod +x /{* app_name *}/jobs/*.sh

# If GOSU_USER environment variable set to something other than 0:0 (root:root),
# become user:group set within and exec command passed in args
if [ "$GOSU_USER" != "0:0" ]; then
    chown -R $GOSU_USER /{* app_name *}
    exec /usr/local/bin/gosu $GOSU_USER "$@"
else
    # If GOSU_USER was 0:0 exec command passed in args without gosu (assume already root)
    exec "$@"
fi
