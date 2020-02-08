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
