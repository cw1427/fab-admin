"""
Created on {* now *}.
@desc: commands module
@app: {* app_name *}
"""

import click

import logging
from . import appbuilder
from fab_admin.console import cli_app

log = logging.getLogger(appbuilder.get_app.config['LOG_NAME'])


@cli_app.command("hello")
def say_hi():
    """Sample customization app command."""
    click.echo('Sample command')
    with appbuilder.get_app.app_context():
        click.echo('Hi, have fun!')


# @cli_app.command("ssehb")
# def sse_heart_beat():
#     """The heart beat command to check the invalid subscribe."""
#     from . import sse
#     click.echo('{0}:start sse heart beat polling.'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
#     with appbuilder.get_app.app_context():
#         sse.heart_beat()
#     click.echo('{0}:finish sse heart beat polling.'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

#
# @cli_app.command("syncauth")
# def sync_auth_redis():
#     """Try to sync fab auth structure data into redis"""
#     from . import redis_main
#     from fab_admin.models import MyUser
#     from sqlalchemy.orm import joinedload
#     from flask_appbuilder.security.sqla.models import Role, PermissionView, Permission, ViewMenu
#     import re
#     import datetime
#     with appbuilder.get_app.app_context():
#         # user list with joinedload roles by extinfo only need cache user with apikey.
#         users = appbuilder.get_session.query(MyUser).options(joinedload(MyUser.extinfo), joinedload(MyUser.roles)).all()
#         u_apik = {}
#         for u in users:
#             if u.extinfo and u.extinfo.api_key:
#                 u_apik["apikey_" + u.extinfo.api_key] = u.to_json()
#                 u_apik["apikey_" + u.extinfo.api_key]['extinfo'] = u.extinfo.to_json()
#                 u_apik["apikey_" + u.extinfo.api_key]['roles'] = [r.to_json() for r in u.roles]
#                 u_apik["apikey_" + u.extinfo.api_key]['cache'] = True
#         role_pv_subquery = appbuilder.get_session.query(Role, PermissionView.permission_id, \
#                         PermissionView.view_menu_id).outerjoin(Role.permissions).subquery()
#         role_pv = appbuilder.get_session.query(role_pv_subquery, Permission.name, ViewMenu.name). \
#                 join(Permission).join(ViewMenu).all()
#         r_pv = {}
#         # the result would be tuple list like: (2, 'Public', 13, 36, 'menu_access', 'AutoDocumentsView')
#         # rejson doesn't support for jsonpath filter, change the structure index by p$v:role
#         for r in role_pv:
#             json_key = "{0}${1}".format(re.sub(appbuilder.get_app.config['FAB_AUTH_KEY_REPLACE_PATTERN'], '', r[4]), \
#                                         re.sub(appbuilder.get_app.config['FAB_AUTH_KEY_REPLACE_PATTERN'], '', r[5]))
#             if r_pv.get(json_key):
#                 r_pv[json_key].append(r[1])
#             else:
#                 r_pv[json_key] = [r[1]]
#         pipe = redis_main.pipeline()
#         pipe.jsonset(appbuilder.get_app.config['FAB_AUTH_REDIS_UAPIK_KEY'], '.', u_apik)
#         pipe.jsonset(appbuilder.get_app.config['FAB_AUTH_REDIS_RPV_KEY'], '.', r_pv)
#         pipe.expire(appbuilder.get_app.config['FAB_AUTH_REDIS_UAPIK_KEY'], 360)
#         pipe.expire(appbuilder.get_app.config['FAB_AUTH_REDIS_RPV_KEY'], 360)
#         pipe.execute()
#         click.echo('[{0}] finish sync auth in redis'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
