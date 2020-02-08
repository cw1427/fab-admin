"""
common models  module.
Created on {* now *}.
@desc: your app basic modules
@app: {* app_name *}
"""
# from fab_admin import monkey_patch
# monkey_patch.patch_all()

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who

"""
import os
from fab_admin.utils import dynamic_import_by_patten

dynamic_import_by_patten(os.path.dirname(__file__), 'models_*')
