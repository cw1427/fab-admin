"""
App config module.
Created on {* now *}.
@desc: define your app config item, or overwrite the config in config_base
@app name: {* app_name *}
"""

import os
import config_base
from config_base import version, config_local

class config(config_base.config):
    """Customize your config."""
    SECRET_KEY = '{* secret_key *}'
    REDISSN = 'mymaster'
    REDISPASS = os.environ.get('REDIS_PASSWORD', config_local.REDISPASS if config_local else None)
    # default just use Redis schema, but we support for redis+sentinel schema
    REDIS_URL = os.environ.get('REDIS_URL', \
                               "redis://:{0}@localhost:26379/{1}/0".format(REDISPASS, REDISSN))
    SSE_REDIS_URL = os.environ.get('SSE_REDIS_URL', \
                                "redis://:{0}@localhost:6379/{1}/1".format(REDISPASS, REDISSN))
    RQ_REDIS_URL = os.environ.get('RQ_REDIS_URL', \
                                "redis://:{0}@localhost:6379/{1}/2".format(REDISPASS, REDISSN))
