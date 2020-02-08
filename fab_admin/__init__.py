"""
Fab_admin skeleton application.
Created on 2020-01-19.
desc: try to make a monkey patch when import this base module
author: Shawn Chen.
"""
from fab_admin import monkey_patch
monkey_patch.patch_all()
from fab_admin.utils import create_app

app, appbuilder = create_app('fab_admin.config.config')
