"""
Basic views.
Created on {* now *}.
@desc: A sample Views module.
@app: {* app_name *}
"""
import os
from . import appbuilder, autodoc
import logging
from flask_appbuilder.baseviews import expose
from flask_appbuilder.views import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.security.decorators import permission_name, has_access_api
from flask import request
from flask.json import jsonify
from sqlalchemy.sql.expression import and_, text, or_
from flask.helpers import make_response
from .models_sample import SampleBenchmark
import datetime

"""
    Create your Views::
    A sample view

"""


log = logging.getLogger(appbuilder.get_app.config['LOG_NAME'])


class SampleView(ModelView):
    """fab_admin sample business view class."""

    route_base = "/sample"
    datamodel = SQLAInterface(SampleBenchmark)

    @expose('/api/upload', methods=['PUT', 'POST'])
    @has_access_api
    @permission_name('SampleCRUD')
    @autodoc.doc(endpoint='SampleView.sample_benchmark_upload', groups='Sample')
    def sample_benchmark_upload(self):
        """
        {
            "desc": "RESTFul api for Sample view benchmark upload",
            "mediaType": "application/json",
            "data": {
                        "ben_server": "ben_server",
                        "server": "server1.com",
                        "site": "site1",
                        "operation": "git clone",
                        "start": 1572837073,
                        "end": 1572860762
                    }
        }
        """
        try:
            data = request.get_json()
            args = dict()
            args['ben_server'] = data['ben_server']
            args['server'] = data['server']
            args['operation'] = data['operation']
            args['site'] = data['site']
            args['start'] = data['start']
            args['end'] = data['end']
            self.datamodel.session.add(SampleBenchmark(**args))
            self.datamodel.session.commit()
        except Exception as e:
            log.error(e)
            return make_response(jsonify({'code': 400, 'message': str(e)}), 400)
        return jsonify({'code': 200, 'message': 'Success'})

    @expose('/api/list', methods=['GET', 'PUT', 'POST'])
    @has_access_api
    @permission_name('SampleCRUD')
    @autodoc.doc(endpoint='SampleView.api_list', groups='Sample')
    def api_list(self):
        """
        {
            "desc": "RESTFul api for Sample benchmark list fetch",
            "mediaType": "application/json",
            "data": {
                "rows": [
                     {
                        "ben_server": "ben_server",
                        "server": "server1.com",
                        "site": "site1",
                        "operation": "git clone",
                        "start": 1572837073,
                        "end": 1572860762
                    }
                ],
                "total": 1
            }
        }
        """
        data = request.values
        query = self.datamodel.session.query(SampleBenchmark)
        search_obj = data.get('search')
        offset = data.get('offset')
        limit = data.get('limit')
        sort = data.get('sort')
        order = data.get('order')
        if search_obj:
            query = query.filter(or_(SampleBenchmark.ben_server.like('%{0}%'.format(search_obj)), \
                                     SampleBenchmark.server.like('%{0}%'.format(search_obj)), \
                                     SampleBenchmark.site.like('%{0}%'.format(search_obj))))
        total = query.count()
        #----order
        if sort and order:
            query = query.order_by(text('{0} {1}'.format(sort, order)))
        #----page offset
        if offset and limit:
            query = query.limit(limit)
            query = query.offset(offset)
        records = query.all()
        return jsonify({'rows': [{'id': b.id, 'ben_server': b.ben_server, 'server': b.server, 'site': b.site, \
                                  'operation': b.operation, 'start': self._format_datetime('%Y-%m-%d %H:%M:%S', b.start), \
                                  'end': self._format_datetime('%Y-%m-%d %H:%M:%S', b.end)} for b in records], \
                        'total': total})

    def _format_datetime(self, pattern, ts):
        return datetime.datetime.fromtimestamp(ts).strftime(pattern) if ts else None

appbuilder.add_view_no_menu(SampleView, "SampleView")
