"""
Created on 2018-6-27.
@desc: fab_admin commands extension to provide clone feature make a basic app based on fabadmin
@author: chenwen9
"""

import os
import click
from . import appbuilder
import logging
import fab_admin
from fab_admin.console import cli_app


log = logging.getLogger(appbuilder.get_app.config['LOG_NAME'])


@cli_app.command("ssehb")
def sse_heart_beat():
    """The heart beat command to check the invalid subscribe."""
    from app import appbuilder, redis_master
    from fab_admin.addon.sse import sse
    import datetime
    click.echo('{0}:start sse heart beat polling.'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    with appbuilder.get_app.app_context():
        sse.heart_beat()
    click.echo('{0}:finish sse heart beat polling.'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


@cli_app.command("syncauth")
def sync_auth_redis():
    """Try to sync fab auth structure data into redis"""
    from app import appbuilder, redis_master
    from fab_admin.models import MyUser
    from sqlalchemy.orm import joinedload
    from flask_appbuilder.security.sqla.models import Role, PermissionView, Permission, ViewMenu
    import re
    import datetime
    with appbuilder.get_app.app_context():
        # user list with joinedload roles by extinfo only need cache user with apikey.
        users = appbuilder.get_session.query(MyUser).options(joinedload(MyUser.extinfo), joinedload(MyUser.roles)).all()
        u_apik = {}
        for u in users:
            if u.extinfo and u.extinfo.api_key:
                u_apik["apikey_" + u.extinfo.api_key] = u.to_json()
                u_apik["apikey_" + u.extinfo.api_key]['extinfo'] = u.extinfo.to_json()
                u_apik["apikey_" + u.extinfo.api_key]['roles'] = [r.to_json() for r in u.roles]
                u_apik["apikey_" + u.extinfo.api_key]['cache'] = True
        role_pv_subquery = appbuilder.get_session.query(Role, PermissionView.permission_id, \
                        PermissionView.view_menu_id).outerjoin(Role.permissions).subquery()
        role_pv = appbuilder.get_session.query(role_pv_subquery, Permission.name, ViewMenu.name). \
                join(Permission).join(ViewMenu).all()
        r_pv = {}
        # the result would be tuple list like: (2, 'Public', 13, 36, 'menu_access', 'AutoDocumentsView')
        # rejson doesn't support for jsonpath filter, change the structure index by p$v:role
        for r in role_pv:
            json_key = "{0}${1}".format(re.sub(appbuilder.get_app.config['FAB_AUTH_KEY_REPLACE_PATTERN'], '', r[4]), \
                                        re.sub(appbuilder.get_app.config['FAB_AUTH_KEY_REPLACE_PATTERN'], '', r[5]))
            if r_pv.get(json_key):
                r_pv[json_key].append(r[1])
            else:
                r_pv[json_key] = [r[1]]
        pipe = redis_master.pipeline()
        pipe.jsonset(appbuilder.get_app.config['FAB_AUTH_REDIS_UAPIK_KEY'], '.', u_apik)
        pipe.jsonset(appbuilder.get_app.config['FAB_AUTH_REDIS_RPV_KEY'], '.', r_pv)
        pipe.expire(appbuilder.get_app.config['FAB_AUTH_REDIS_UAPIK_KEY'], 360)
        pipe.expire(appbuilder.get_app.config['FAB_AUTH_REDIS_RPV_KEY'], 360)
        pipe.execute()
        click.echo('[{0}] finish sync auth in redis'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


@cli_app.command("clone")
@click.option('--name', '-n', default='fabadmin', help="The app name you want to created")
@click.option('--address', '-a', default='localhost', help="The app front-end will call the backend address")
@click.option('--force', '-f', is_flag=True, default=False, help="force clone if there already has app folder")
def clone_fabadmin_app(name, address, force):
    """
        Clone a basic fab_admin app
    """
    import glob
    from pathlib import Path
    import shutil
    import datetime
    import jinja2
    from werkzeug.security import gen_salt
    # check if there already has app folder in the current folder
    if os.path.exists(os.path.join(os.getcwd(), 'app')) and (not force):
        click.echo('There already has app in current dir, inpurt --force to force clone the app')
        return

    render_data = {'app_name': name, 'now': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                   'secret_key': gen_salt(64), 'fab_admin_path': fab_admin.__path__[0], 'address': address}
    template_path = os.path.join(fab_admin.__path__[0], 'app_templates')
    templateLoader = jinja2.FileSystemLoader(searchpath=template_path)
    templateEnv = jinja2.Environment(loader=templateLoader, variable_start_string='{*', variable_end_string='*}')
    for file_path in glob.iglob(os.path.join(template_path, '**'), recursive=True):
        target_file_path = file_path.replace(template_path, os.getcwd())
        ori_path = Path(file_path)
        if ori_path.is_file():
            target_file_path = file_path.replace(template_path, os.getcwd())
            if ori_path.suffix in ['.pyc']:
                continue
            elif ori_path.suffix in ['.conf', '.ini', '.py', '.yml', '.bat', '.rst', '.gradle', '.sh', '.bash', '.json', '.vue',
                '.properties'] or file_path in [os.path.join(template_path, 'app', 'templates', 'vue', 'index.html'),
                                                os.path.join(template_path, 'app', 'public', 'public', 'index.html'),
                                                os.path.join(template_path, 'app', 'public', 'vue.config.js'),
                                                os.path.join(template_path, 'app', 'public', 'config', 'url.js')]:
                _render_file(templateEnv, file_path.replace(template_path, ''), target_file_path, render_data)
            elif ori_path.name in ['Dockerfile']:
                _render_file(templateEnv, file_path.replace(template_path, ''), target_file_path, render_data)
            else:
                shutil.copyfile(file_path, target_file_path)
        else:
            Path(target_file_path).mkdir(parents=True, exist_ok=True)
    # render the hiddern files
    for file_path in glob.iglob(os.path.join(template_path, '**/.*'), recursive=True):
        target_file_path = file_path.replace(template_path, os.getcwd())
        shutil.copyfile(file_path, target_file_path)


def _render_file(env, path, dest_path, render_data):
    """jinja render file"""
    content = env.get_template(path.replace('\\', '/')).render(render_data)
    with open(dest_path, mode='w', encoding="utf-8") as f:
        f.write(content)
