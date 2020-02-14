"""
Created on 2018-8-12.
Configuration Center View layer
@author: chenwen9
"""
import logging
from app import appbuilder, autodoc, redis_master, redis_slave
from fab_admin.models import ConfItem
from flask_appbuilder.baseviews import expose, BaseView
from flask_appbuilder.security.decorators import has_access_api, permission_name
from flask import jsonify
from flask.globals import g, request
import json
import time

log = logging.getLogger(appbuilder.get_app.config['LOG_NAME'])
CONF_PROJECTS_KEY_FORMAT = "cfg:projects"
CONF_KEY_FORMAT = "cfg:{p}:{k}"
CONF_KEY_HISTORY_LIST_FORMAT = "cfg:{p}:{k}:history"
CONF_PROJECT_KEYSET_FORMAT = "cfg:{p}:keyset"
CONF_PROJECT_WRITE_PERM_FORMAT = "cfg:{p}:perm:write"
CONF_PROJECT_READ_PERM_FORMAT = "cfg:{p}:perm:read"


class ConfCenterView(BaseView):
    """The Config center fab view module."""

    route_base = "/conf"

    @expose('/api/addproject/<project>')
    @has_access_api
    def add_project(self, project=None):
        """Add confcenter project api method."""
        if project and not ' ' in project:
            if redis_slave.sismember(CONF_PROJECTS_KEY_FORMAT, project):
                return jsonify({'message': 'project name exists'}), 400
            else:
                pipe = redis_master.pipeline()
                pipe.sadd(CONF_PROJECTS_KEY_FORMAT, project)
                pipe.sadd(CONF_PROJECT_WRITE_PERM_FORMAT.format(p=project), g.user.username)
                pipe.sadd(CONF_PROJECT_READ_PERM_FORMAT.format(p=project), g.user.username)
                pipe.execute()
                log.info("Successfully add project {p} by {u}".format(p=project, u=g.user.username))
                return jsonify({'code': 200, 'message': 'success'})
        else:
            return jsonify({'message': 'project parameter wrong'}), 400

    @expose('/api/getprojects')
    @has_access_api
    @permission_name('confcenterRead')
    def get_projects(self):
        """fetch all of the project lists by permission."""
        #---scan the projects key
        available_proj = []
        for proj in redis_slave.sscan_iter(CONF_PROJECTS_KEY_FORMAT):
            if self._check_conf_permission(proj, 'read'):
                available_proj.append(proj)
        return jsonify({'code': 200, 'data': available_proj})

    @expose('/api/addconfig/<project>', methods=['POST'])
    @has_access_api
    @permission_name('confcenterWrite')
    def add_configs_byproject(self, project):
        """add config item by project api method."""
        if redis_slave.sismember(CONF_PROJECTS_KEY_FORMAT, project):
            if self._check_conf_permission(project, 'write'):
                data = request.get_json()
                if data.get('name') and data.get('value'):
                    if not self._check_conf_exists(project, data['name']):
                        try:
                            value = json.loads(data.get('value'))
                        except Exception:
                            value = data.get('value')
                        item = ConfItem(project, data.get('name'), value)
                        #---we are going to use rejson to wrap the use custmize config item value into JSON type
                        pipe = redis_master.pipeline()
                        pipe.jsonset(CONF_KEY_FORMAT.format(p=project, k=data.get('name')), '.', item)
                        pipe.sadd(CONF_PROJECT_KEYSET_FORMAT.format(p=project), data.get('name'))
                        pipe.execute()
                        log.info("Successfully add config {c} for project {p} by {u}".format(c=data.get('name'), \
                                                                                    p=project, u=g.user.username))
                        return jsonify({'message': 'success'})
                    else:
                        return jsonify({'message': 'Key exists'}), 400
                else:
                    return jsonify({'message': 'Wrong parameter data'}), 400
            else:
                return jsonify({'message': 'doesn\'t have permission'}), 403
        else:
            return jsonify({'message': 'project does not exists'}), 400

    @expose('/api/updateconfig/<project>', methods=['POST'])
    @has_access_api
    @permission_name('confcenterWrite')
    def update_configs_byproject(self, project):
        """update config value by project and config key."""
        if redis_slave.sismember(CONF_PROJECTS_KEY_FORMAT, project.strip()):
            if self._check_conf_permission(project, 'write'):
                data = request.get_json()
                if data.get('name') and data.get('value'):
                    if self._check_conf_exists(project, data['name']):
                        #---key history is a kind of json list, which item is one of the ConfItem value.
                        ori_item = redis_slave.jsonget(CONF_KEY_FORMAT.format(p=project, k=data.get('name')))
                        if redis_slave.exists(CONF_KEY_HISTORY_LIST_FORMAT.format(p=project, k=data.get('name'))):
                            redis_master.jsonarrinsert(CONF_KEY_HISTORY_LIST_FORMAT.format(p=project, \
                                                                                k=data.get('name')), '.', 0, ori_item)
                        else:
                            redis_master.jsonset(CONF_KEY_HISTORY_LIST_FORMAT.format(p=project, k=data.get('name')), \
                                                 '.', [ori_item])
                        try:
                            value = json.loads(data.get('value'))
                        except Exception:
                            value = data.get('value')
                        pipe = redis_master.pipeline()
                        pipe.jsonset(CONF_KEY_FORMAT.format(p=project, k=data.get('name')), '.value', value)
                        pipe.jsonset(CONF_KEY_FORMAT.format(p=project, k=data.get('name')), '.changed_on', time.time())
                        pipe.jsonset(CONF_KEY_FORMAT.format(p=project, k=data.get('name')), '.changed_by', \
                                     g.user.username)
                        pipe.execute()
                        log.info("Successfully update config {c} for project {p} by {u}". \
                                 format(c=data.get('name'), p=project, u=g.user.username))
                        return jsonify({'message': 'success'})
                    else:
                        return jsonify({'message': 'Key does not exists'}), 400
                else:
                    return jsonify({'message': 'Wrong parameter data'}), 400
            else:
                return jsonify({'message': 'doesn\'t have permission'}), 403
        else:
            return jsonify({'message': 'project doesn\'t exists'}), 400

    @expose('/api/getconfig/<project>/<name>')
    @has_access_api
    @permission_name('confcenterRead')
    @autodoc.doc(endpoint='ConfCenterView.get_config_byproject', groups='Confcenter')
    def get_config_byproject(self, project, name):
        """
        {
            "desc": "RESTFul api for config retrieve by transfer project name the key name in the url <br/> \
                     1. {project} parameter is the config project name, <br/> \
                     2. {name} parameter is the key name <br/> \
                     3. The response data is what the config data setup, please refer the {Sample data} Tag <br/> \
                     4. It will support for the json data subnode(json path) searching soon",
            "mediaType": "application/json",
            "data": {
                        "data" : {
                            "age": 100,
                             "job": "lenovo"
                             }
                    }
        }
        """
        if redis_slave.sismember(CONF_PROJECTS_KEY_FORMAT, project.strip()):
            if self._check_conf_permission(project, 'read'):
                try:
                    value = redis_slave.jsonget(CONF_KEY_FORMAT.format(p=project, k=name), '.value')
                    if value:
                        return jsonify({'data': value})
                    else:
                        return jsonify({'message': 'key does not exists'}), 404
                except Exception as e:
                    log.error(e)
                    return jsonify({'message': 'key not found error= {0}'.format(e)}), 404
            else:
                return jsonify({'message': 'doesn\'t have permission'}), 403
        else:
            return jsonify({'message': 'project doesn\'t exists'}), 400

    @expose('/api/getallconfig/<project>')
    @has_access_api
    @permission_name('confcenterRead')
    def get_allconfig_byproject(self, project):
        """get all config item by project name."""
        if redis_slave.sismember(CONF_PROJECTS_KEY_FORMAT, project.strip()):
            if self._check_conf_permission(project, 'read'):
                try:
                    confs = []
                    for key in redis_slave.sscan_iter(CONF_PROJECT_KEYSET_FORMAT.format(p=project)):
                        confs.append(redis_slave.jsonget(CONF_KEY_FORMAT.format(p=project, k=key)))
                    return jsonify({'data': confs})
                except Exception as e:
                    log.error(e)
                    return jsonify({'message': 'Internal error {0}'.format(e)}), 500
            else:
                return jsonify({'message': 'doesn\'t have permission'}), 403
        else:
            return jsonify({'message': 'project doesn\'t exists'}), 400

    @expose('/api/getpermission/<project>')
    @has_access_api
    def get_project_permission(self, project):
        """get the project permission list reader and writer."""
        if redis_slave.sismember(CONF_PROJECTS_KEY_FORMAT, project.strip()):
            writer = redis_slave.smembers(CONF_PROJECT_WRITE_PERM_FORMAT.format(p=project))
            reader = redis_slave.smembers(CONF_PROJECT_READ_PERM_FORMAT.format(p=project))
            return jsonify({"reader": list(reader), "writer": list(writer)})
        else:
            return jsonify({'message': 'project doesn\'t exists'}), 400

    @expose('/api/updatepermission/<project>', methods=['POST'])
    @has_access_api
    def update_project_permission(self, project):
        """update project permission list by project and the permision catagory."""
        if redis_slave.sismember(CONF_PROJECTS_KEY_FORMAT, project.strip()):
            data = request.get_json()
            if data.get('perm') and data.get('users'):
                if data.get('perm') == 'write':
                    conf_proj_perm_key = CONF_PROJECT_WRITE_PERM_FORMAT
                elif  data.get('perm') == 'read':
                    conf_proj_perm_key = CONF_PROJECT_READ_PERM_FORMAT
                else:
                    return jsonify({'message': 'wrong permission params'}), 400
                pipe = redis_master.pipeline()
                pipe.delete(conf_proj_perm_key.format(p=project))
                pipe.sadd(conf_proj_perm_key.format(p=project), *data.get('users'))
                pipe.execute()
                log.info("Successfully update project permission for project {p} by {u}".format(p=project, \
                                                                                                u=g.user.username))
                return jsonify({'message': 'success'})
            else:
                return jsonify({'message': 'wrong parameters'}), 400
        else:
            return jsonify({'message': 'project doesn\'t exists'}), 400

    @expose('/api/delconfig/<project>/<name>', methods=['DELETE'])
    @has_access_api
    @permission_name('confcenterWrite')
    def del_config_byproject(self, project, name):
        """delte config by project name."""
        if redis_slave.sismember(CONF_PROJECTS_KEY_FORMAT, project.strip()):
            if self._check_conf_permission(project, 'write'):
                try:
                    #----delete the project item and its history
                    del_keys = [CONF_KEY_FORMAT.format(p=project, k=name), \
                                CONF_KEY_HISTORY_LIST_FORMAT.format(p=project, k=name)]
                    pipe = redis_master.pipeline()
                    pipe.delete(*del_keys)
                    pipe.srem(CONF_PROJECT_KEYSET_FORMAT.format(p=project), name)
                    pipe.execute()
                    log.info("Successfully delete project config for project {p} by {u}".format(p=project, \
                                                                                                u=g.user.username))
                    return jsonify({'message': 'success'})
                except Exception as e:
                    log.error(e)
                    return jsonify({'message': 'delete item  error= {0}'.format(e)}), 500
            else:
                return jsonify({'message': 'doesn\'t have permission'}), 403
        else:
            return jsonify({'message': 'project doesn\'t exists'}), 400

    @expose('/api/delproj/<project>', methods=['DELETE'])
    @has_access_api
    @permission_name('confcenterWrite')
    def del_project_byname(self, project):
        """delte all the project by name."""
        if redis_slave.sismember(CONF_PROJECTS_KEY_FORMAT, project.strip()):
            if self._check_conf_permission(project, 'write'):
                try:
                    #----get this projects keyset
                    keys = redis_slave.smembers(CONF_PROJECT_KEYSET_FORMAT.format(p=project))
                    for name in keys:
                        del_keys = [CONF_KEY_FORMAT.format(p=project, k=name), CONF_KEY_HISTORY_LIST_FORMAT. \
                                    format(p=project, k=name)]
                        redis_master.delete(*del_keys)
                    redis_master.delete(CONF_PROJECT_KEYSET_FORMAT.format(p=project), CONF_PROJECT_WRITE_PERM_FORMAT. \
                                        format(p=project), CONF_PROJECT_READ_PERM_FORMAT.format(p=project))
                    redis_master.srem(CONF_PROJECTS_KEY_FORMAT, project)
                    log.info("Successfully delete project byname for project {p} by {u}".format(p=project, \
                                                                                                u=g.user.username))
                    return jsonify({'message': 'success'})
                except Exception as e:
                    log.error(e)
                    return jsonify({'message': 'delete item  error= {0}'.format(e)}), 500
            else:
                return jsonify({'message': 'doesn\'t have permission'}), 403
        else:
            return jsonify({'message': 'project doesn\'t exists'}), 400

    def _check_conf_permission(self, project, perm):
        """inner method check mermission."""
        # if is Admin role direct allow
        for role in g.user.roles:
            if appbuilder.get_app.config['AUTH_ROLE_ADMIN'] == role.name:
                return True
        return redis_slave.sismember("cfg:{0}:perm:{1}".format(project, perm), g.user.username)

    def _check_conf_exists(self, project, key):
        """inner method check config exists or not."""
        return redis_slave.exists(CONF_KEY_FORMAT.format(p=project, k=key))


appbuilder.add_view_no_menu(ConfCenterView)
