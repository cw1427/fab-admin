"""
Created on {* now *}
@desc: common sse Views (server-side send event)
@app: {* app_name *}
"""
from flask_appbuilder.baseviews import  expose, BaseView
import logging

from .sse import sse
from flask.json import jsonify
from flask.globals import request
from fab_admin.security_manager import login_required_api
from flask_appbuilder.security.decorators import permission_name

log = logging.getLogger(__name__)


class SSEView(BaseView):
    """SSE Viewmodel class"""

    route_base = "/sse"

    @login_required_api
    @expose('/api/subscribe', methods=['GET', 'POST'])
    @expose('/api/subscribe/<string:channel>', methods=['GET', 'POST'])
    def stream(self, channel=None):
        #----check if there are existing redis connections.
        return sse.stream(channel)

    @expose('/api/publish/<string:channel>', methods=['PUT', 'POST'])
    @permission_name('sse_publish')
    def publish(self, channel):
        try:
            data = request.get_json()
            content = data['content']
            type = data.get('type')
            id = data.get('id')
            retry = data.get('retry')
            sse.publish(content, type, id, retry, channel)
        except Exception as e:
            log.error(e)
            return jsonify({'code': 400, 'message': str(e)}), 400
        return jsonify({'message': 'success'})
