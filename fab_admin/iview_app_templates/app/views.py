"""
Basic views.
Created on {* now *}.
@desc: your basic views.
@app: {* app_name *}
"""
import os
from . import appbuilder
import logging
from fab_admin.views import ApiUserView
from flask.templating import render_template
from fab_admin.utils import dynamic_import_by_patten, dynamic_import_by_name

"""
    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(MyModelView, "My View", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
"""

"""
    Application wide 404 error handler
"""


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    """The global page not found flask action."""
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

log = logging.getLogger(appbuilder.get_app.config['LOG_NAME'])

appbuilder.add_view_no_menu(ApiUserView)
dynamic_import_by_patten(os.path.dirname(__file__), 'views_*')
for views_addon in appbuilder.get_app.config['ADDON_VIEWS']:
    dynamic_import_by_name(views_addon, module_prefix='fab_admin')
