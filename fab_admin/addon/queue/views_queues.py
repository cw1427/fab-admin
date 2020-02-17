"""
Redis queue views.
Created on 2020-02-17.
@desc: Redis queue views.
@app: fab_admin
"""
from flask_appbuilder.baseviews import  expose, BaseView
from flask_appbuilder.security.decorators import permission_name, has_access_api
import logging

from app import appbuilder, autodoc
from flask.json import jsonify
from flask import render_template
import pytz
import datetime
from fab_admin.addon.queue.queues import schedule_requests_task, schedule_test_task
from requests.auth import HTTPBasicAuth
import rq_dashboard
import rq_scheduler_dashboard
from rq.compat import text_type
from uuid import uuid4
from flask_login import current_user
from flask.globals import request

log = logging.getLogger(appbuilder.get_app.config['LOG_NAME'])


class QueuesView(BaseView):
    """Queues Viewmodel class"""

    route_base = "/queue"

    @expose('/api/atreq/<string:at>', methods=['POST'])
    @has_access_api
    @permission_name('atreq')
    @autodoc.doc(endpoint='QueuesView.at_requests', groups='Tasks')
    def at_requests(self, at):
        """
        {
            "desc": "AT request tasks entrance point. <br/> \
            It would provide at (linux command) feature to help you reserve a request event by your parameter.<br/> \
            It needs a json data have (url,method,auth,header,data) properties. <br/> \
            The auth and header are optional property. <br/> \
            Parameter:  at=20190502133000 it means when at that time the task would occurred. <br/> \
            The at parameter format should be: %Y%m%d%H%M%S",
            "mediaType": "application/json",
            "data": {
                        "url": ".....",
                        "method": "post",
                        "auth": "user:pass",
                        "header": {"apikey": "****"},
                        "data": {"parame1":"value1","parame2":"value2"}
                    }
        }
        """
        try:
            if len(at) != 14:
                raise Exception('Wrong datetime format, it should be %Y%m%d%H%M%S')
            at = datetime.datetime.strptime(at, "%Y%m%d%H%M%S")
            at = at.astimezone(pytz.utc)
#             at = pytz.timezone('America/Chicago').localize(at).astimezone(pytz.utc)
        except Exception as e:
            log.error("format parameter at error=%s", e)
            return jsonify({'message': 'Wrong parameter, it should be %Y%m%d%H%M%S', 'code': 400}), 400
        try:
            data = request.get_json()
            basic_auth = data.get('auth', None)
            if basic_auth:
                basic_auth = basic_auth.split(':')
                basic_auth = HTTPBasicAuth(basic_auth[0], basic_auth[1])
            header = data.get('header', None)
            job_id = text_type(uuid4())
            schedule_requests_task.schedule(at, data['url'], data['method'], basic_auth, header, \
                                            job_id=job_id, **data['data'])
        except Exception as e:
            log.error(e)
            return jsonify({'code': 400, 'message': str(e)}), 400

        return jsonify({'message': 'success', 'id': job_id})

    @expose('/api/attest/<string:at>', methods=['POST'])
    @has_access_api
    @permission_name('atreq')
    def at_test(self, at):
        """
        Test schedule_requests_task execution test Flask-rq2 post fork feature
        """
        try:
            if len(at) != 14:
                raise Exception('Wrong datetime format, it should be %Y%m%d%H%M%S')
            at = datetime.datetime.strptime(at, "%Y%m%d%H%M%S")
            at = at.astimezone(pytz.utc)
        except Exception as e:
            log.error("format parameter at error=%s", e)
            return jsonify({'message': 'Wrong parameter, it should be %Y%m%d%H%M%S', 'code': 400}), 400
        try:
            data = request.get_json()
            name = data.get('name', None)
            job_id = text_type(uuid4())
            schedule_test_task.schedule(at, name, job_id=job_id)
        except Exception as e:
            log.error(e)
            return jsonify({'code': 400, 'message': str(e)}), 400

        return jsonify({'message': 'success', 'id': job_id})

appbuilder.add_view_no_menu(QueuesView)


@rq_dashboard.blueprint.before_request
@rq_scheduler_dashboard.blueprint.before_request
def check_auth():
    """dashboard permission checking interceptor."""
    if not current_user.is_authenticated:
        return render_template('401.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 401
    for role in current_user.roles:
        if appbuilder.get_app.config['AUTH_ROLE_ADMIN'] == role.name:
            return None
    return render_template('403.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 403
appbuilder.get_app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")
appbuilder.add_link('tasks_queue', href="/rq", label="tasks in queue", category="Queues")
appbuilder.get_app.register_blueprint(rq_scheduler_dashboard.blueprint, url_prefix="/scheduler")
appbuilder.add_link('schedule_queue', href="/scheduler", label="schedule in queue", category="Queues")
