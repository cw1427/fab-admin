export PYTHONPATH=/fabadmin
export FLASK_APP=wsgi_handler:app
if [ -f ${DB_PWD_FILE} ]; then
    export DB_PWD=$(cat ${DB_PWD_FILE})
fi
