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


@cli_app.command("clone")
@click.option('--name', '-n', default='fabadmin', help="The app name you want to created")
@click.option('--force', '-f', is_flag=True, default=False, help="force clone if there already has app folder")
def clone_fabadmin_app(name, force):
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
                   'secret_key': gen_salt(64), 'fab_admin_path': fab_admin.__path__[0]}
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
            elif ori_path.suffix in ['.py', '.yml', '.bat', '.rst', '.gradle', '.sh', '.bash', '.json', '.vue',
                '.properties'] or file_path in [os.path.join(template_path, 'app', 'public', 'public', 'index.html'),
                                                os.path.join(template_path, 'app', 'public', 'vue.config.js')]:
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
