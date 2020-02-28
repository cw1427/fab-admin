"""
Fab_admin skegeton application.
Created on {* now *}.
desc: try to make a monkey patch when import this base module
@app: {* app_name *}
"""
from fab_admin import monkey_patch
monkey_patch.patch_all()
import os
import sys
import logging
import base64
from flask import Flask, request, session, _request_ctx_stack
from flask_login import LoginManager, current_user, login_user
from fab_admin.models import CustomJsonEncoder
from fab_admin.utils import create_app, redis_sentinel_client_factory
from flask_appbuilder import Base
from flask_rq2.app import RQ
from sqlalchemy.orm import joinedload, contains_eager
from sqlalchemy.sql.expression import and_

app, appbuilder = create_app('config.config', app_name='app')
log = logging.getLogger(appbuilder.get_app.config['LOG_NAME'])
autodoc = app.extensions['autodoc']
app.config.setdefault('REDIS_ENCODER', CustomJsonEncoder())
# primary redis clients
redis_master, redis_slave = redis_sentinel_client_factory(app, service_name=app.config['REDISSN'])
# sse redis client
sse_master, _ = redis_sentinel_client_factory(app, service_name=app.config['REDISSN'], config_prefix='SSE_REDIS')
app.extensions['sse_master'] = sse_master
# rq redis client
rq_redis_master, _ = redis_sentinel_client_factory(app, service_name=app.config['REDISSN'], config_prefix='RQ_REDIS')
rq = RQ(app, client=rq_redis_master)
from . import views, models
if app.config.get('AUTO_UPDATE_PERM'):
    Base.metadata.create_all(appbuilder.get_session.get_bind(mapper=None, clause=None))
if app.config.get('SECURITY_CLEANUP'):
    log.info("SECURITY CLEANUP enabled, start sync security data into DB")
    appbuilder.security_cleanup()
    log.info("SECURITY CLEANUP enabled, end sync security data into DB")

if app.config['APP_MODE'] == 'DEV':
    try:
        from flask_cors import CORS
        CORS(app, resources=r'*', origins=r'http://{* address *}:8080', supports_credentials=True)

        @app.after_request
        def process_response(response):
            """process response function a Flask after request method."""
            if request.method == 'OPTIONS' and appbuilder.get_app.config['APP_MODE'] == 'DEV' and \
            response.status_code == 301:
                response.status_code = 200
                _request_ctx_stack.top.session.clear()
            return response
    except Exception as e:
        log.error('Load CORS module failed {0}'.format(e))


def load_user_from_request(request):
    """Flask login request customize loader function."""
    # do BSM APIKEY authentication first.  try to check if head have the api_key
    api_key = request.headers.get('X-{* app_name | capitalize *}-Api')
    if api_key:
        session['REST_SESSION'] = True
        try:
            from fab_admin.models import MyUser, UserExtInfo
            from flask_appbuilder.security.sqla.models import Role
            if appbuilder.get_app.config['FAB_AUTH_REDIS_CACHE']:
                # API-KEY auth and Redis cache enable
                user_dict = redis_slave.jsonget(appbuilder.get_app.config['FAB_AUTH_REDIS_UAPIK_KEY'], \
                                                ".apikey_{0}".format(api_key))
                if not user_dict:
                    raise Exception("cache missed")
                log.debug("APIKEY found cache %s", api_key)
                user = MyUser()
                for k, v in user_dict.items():
                    if k == 'extinfo':
                        extinfo = UserExtInfo(**v)
                        user.extinfo = extinfo
                    elif k == 'roles':
                        user.roles = []
                        for role_dict in v:
                            role = Role(**role_dict)
                            user.roles.append(role)
                    else:
                        user.__setattr__(k, v)
                login_user(user, remember=False)
                return user
        except Exception as e:
            log.error('API Key authentication failed for authen={0}:{1}'.format(api_key, str(e)))
        # Back to original authentication
        user = appbuilder.get_session.query(MyUser).join(UserExtInfo, and_(MyUser.id == UserExtInfo.id, \
               UserExtInfo.api_key == api_key)).options(joinedload(MyUser.roles)).one_or_none()
        if user:
            login_user(user, remember=False)
        return user
    # Then try to login using the api_key url arg
    api_key = request.args.get('api_key')
    if api_key:
        session['REST_SESSION'] = True
        user = appbuilder.sm.auth_user_ldap(api_key.split(':')[0], api_key.split(':')[1], True)
        if user:
            login_user(user, remember=False)
        return user
    # Last, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        session['REST_SESSION'] = True
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
            api_key = api_key.decode()
            user = appbuilder.sm.auth_user_ldap(api_key.split(':')[0], api_key.split(':')[1], True)
            if user:
                login_user(user, remember=False)
            return user
        except Exception as e:
            log.error('Basic authentication failed for authen={0}:{1}'.format(api_key, str(e)))
    # finally, return None if both methods did not login the user
    return None


@app.after_request
def per_request_callbacks(response):
    """Flask request callback hook function."""
    #----deal with REST API invoking remove the session save
    if session.get('REST_SESSION', False):
        _request_ctx_stack.top.session.clear()

    return response

appbuilder.sm.lm.request_loader(load_user_from_request)

