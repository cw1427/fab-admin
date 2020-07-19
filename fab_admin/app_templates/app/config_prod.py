"""
Created on {* now *}
@desc: prod scope config
@app: {* app_name *}
"""
import os
import version
from config import config_local
db_user = os.environ.get('DB_USER', 'admin')
db_password = os.environ.get('DB_PWD', '***')
db_host = os.environ.get('DB_HOST', '127.0.0.1:3306')
db_name = os.environ.get('DB_NAME', '{* app_name *}')
APP_NAME = version.APP_NAME
SQLALCHEMY_DATABASE_URI = 'mysql://{0}:{1}@{2}/{3}'.format(db_user, db_password, db_host, db_name)
TEMPLATES_AUTO_RELOAD = False

#---------------------------------------------------
# SQLAlchemy pool config setup for mysql
#---------------------------------------------------
SQLALCHEMY_POOL_SIZE = 100
SQLALCHEMY_POOL_RECYCLE = 1800
SQLALCHEMY_POOL_PRE_PING = True
SQLALCHEMY_MAX_OVERFLOW = 10
SQLALCHEMY_ECHO = False
APP_MODE = 'PRO'
APP_VERSION = '%s:%s' % (APP_MODE, version.VERSION_STRING)
#---security cleanup  would auto sync security data from code to DB
SECURITY_CLEANUP = False
AUTO_UPDATE_PERM = os.environ.get('AUTO_UPDATE_PERM', False)
# redis credential on prod
REDISSN = 'mymain'
REDISPASS = os.environ.get('REDIS_PASSWORD', config_local.REDISPASS if config_local else None)
REDIS_URL = os.environ.get('REDIS_URL', \
                           "redis+sentinel://:{0}@localhost:6379/{1}/0".format(REDISPASS, REDISSN))
SSE_REDIS_URL = os.environ.get('SSE_REDIS_URL', \
                               "redis+sentinel://:{0}@localhost:26379/{1}/1".format(REDISPASS, REDISSN))
RQ_REDIS_URL = os.environ.get('RQ_REDIS_URL', \
                                  "redis+sentinel://:{0}@localhost:26379/{1}/2".format(REDISPASS, REDISSN))
