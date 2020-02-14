import logging
from flask_appbuilder.basemanager import BaseManager
from .views import SSEView

log = logging.getLogger(__name__)

"""
   Create your plugin manager, extend from BaseManager.
   This will let you create your models and register your views

"""


class SSEManager(BaseManager):

    sse_view = SSEView

    def __init__(self, appbuilder):
        """
             Use the constructor to setup any config keys specific for your app.
        """
        super(SSEManager, self).__init__(appbuilder)
        self.appbuilder.get_app.config.setdefault('SSE_KEY', 'sse')

    def register_views(self):
        """
            This method is called by AppBuilder when initializing, use it to add you views
        """
        self.appbuilder.add_view_no_menu(SSEView, "SSEView")

    def pre_process(self):
        pass

    def post_process(self):
        pass

