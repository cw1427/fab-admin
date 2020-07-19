"""
Created on 2020-01-14.

@author: chenwen9
"""
import os
from flask import Flask
from flask_appbuilder import AppBuilder
from flask_session import Session
from flask_redis_sentinel import SentinelExtension
from fab_addon_autodoc.autodoc import Autodoc
from fab_admin.log import Logging
from logging.handlers import RotatingFileHandler
from fab_admin.models import SQLAlchemy
from fab_admin.myredis import MySentinel, BlockingSentinelConnectionPool
from . import security_manager
from rejson.client import Client as redis_client
from pathlib import Path
import logging
import urllib

log = logging.getLogger(__name__)


def create_app(config, app_name='fabadmin'):
    """BSM app factory method."""
    app = Flask(app_name)
    app.config.from_object(config)
    app.config.from_envvar("CONFIG_ENV", silent=True)
    db = SQLAlchemy(app)
    Session(app)
    Autodoc(app)
    Path(os.path.dirname(app.config.get('FLASK_LOG_PATH', os.path.join(os.getcwd(), 'logs',
                                        "fab_admin.log")))).mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(app.config.get('FLASK_LOG_PATH', os.path.join(os.getcwd(),
                                        'logs', "fab_admin.log")), maxBytes=1024 * 1024 * 10, backupCount=13)
    app.config.setdefault('LOG_NAME', 'fabadmin')
    Logging(app, handler)
    return app, AppBuilder(app, db.session, security_manager_class=security_manager.SecurityManager, \
                            update_perms=app.config['AUTO_UPDATE_PERM'], indexview=security_manager.IndexView)


def redis_sentinel_client_factory(app, service_name='mymain', config_prefix='REDIS'):
    """sentinel redis client factory method"""
    parsed_url = urllib.parse.urlparse(app.config.get(f"{config_prefix}_URL"))
    if parsed_url.scheme != 'redis+sentinel':
        # default redis client without sentinel
        from flask_redis import FlaskRedis
        from fab_admin.models import CustomJsonEncoder
        if config_prefix in ['RQ_REDIS']:
            redis_main = redis_subordinate = FlaskRedis.from_custom_provider(redis_client, app, decode_responses=False)
        else:
            redis_main = redis_subordinate = FlaskRedis.from_custom_provider(redis_client, app, decode_responses=True)
            redis_main.setEncoder(CustomJsonEncoder())
            redis_subordinate.setEncoder(CustomJsonEncoder())
#         redis_main = redis_subordinate = redis_sentinel.default_connection
    else:
        redis_sentinel = SentinelExtension(app=app, config_prefix=config_prefix, client_class=redis_client,
                                       sentinel_class=MySentinel)
        redis_main_cp = BlockingSentinelConnectionPool(service_name, redis_sentinel.sentinel)
        redis_main = redis_sentinel.main_for(service_name, connection_pool_obj=redis_main_cp)
        redis_subordinate_cp = BlockingSentinelConnectionPool(service_name, redis_sentinel.sentinel)
        redis_subordinate = redis_sentinel.subordinate_for(service_name, connection_pool_obj=redis_subordinate_cp)
    return redis_main, redis_subordinate


def dynamic_import_by_patten(path, patten, module_prefix='app'):
    """
        dynamic load the modules under the path by patten
    """
    import glob
    from pathlib import Path
    import importlib

    for file_path in glob.iglob(os.path.join(path, patten), recursive=False):
        module_path = Path(file_path)
        importlib.import_module(f'{module_prefix}.' + module_path.name.split('.')[0])
#         spec = importlib.util.spec_from_file_location(module_path.name.split('.')[0], file_path)
#         source_module = importlib.util.module_from_spec(spec)
#         spec.loader.exec_module(source_module)


def dynamic_import_by_name(name,  module_prefix='app'):
    """ dynamic import by name """
    import importlib
    importlib.import_module(f'{module_prefix}.{name}')
