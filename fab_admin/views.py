"""
BSM common view  module.

Created on 2018-2-3.
author: chenwen9.
"""
from flask import render_template, session, request, g, jsonify
from app import appbuilder
from fab_admin.models import MyUser, UserExtInfo
import logging
from fab_admin.security_manager import login_required_api
from flask_appbuilder.baseviews import BaseView, expose
from flask_login import current_user, login_user, login_required, logout_user
from flask.helpers import make_response
from flask_appbuilder.security.decorators import has_access_api, permission_name
from sqlalchemy.sql.expression import or_, text
import os
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.security.sqla.models import Role
from sqlalchemy.sql.functions import func
from werkzeug.security import generate_password_hash
import ldap
from flask_appbuilder.const import LOGMSG_ERR_SEC_AUTH_LDAP_TLS


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
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

log = logging.getLogger(appbuilder.get_app.config['LOG_NAME'])


class ApiUserView(BaseView):
    """The Api user view class, provide the RESTAPI for front-end framework."""

    route_base = '/api'
    datamodel = SQLAInterface(MyUser)

    @expose('/login', methods=['GET', 'POST'])
    def login(self):
        """RESTAPI login action method."""
        if current_user.is_authenticated:
            sid = request.cookies.get(self.appbuilder.get_app.session_cookie_name)
            return jsonify({'token': sid, 'version': self.appbuilder.get_app.config.get('APP_VERSION'), \
                            'sha1': os.environ.get('COMMIT_ID', 'NA')})
        data = request.get_json()
        if data and data.get('userName') and data.get('password'):
            user = self.appbuilder.sm.auth_user_ldap(data['userName'], data['password'])
            if not user:
                return make_response(jsonify({'msg': 'username or password incorrect'}), 401)
            login_user(user, remember=False)
            return jsonify({'token': session.sid, 'version': self.appbuilder.get_app.config.get('APP_VERSION'), \
                            'sha1': os.environ.get('COMMIT_ID', 'NA')})
        else:
            return make_response(jsonify({'msg': 'userName or password parameters error'}), 400)

    @expose('/user_info')
    @login_required_api
    def user_info(self):
        """The user info action RESTAPI method."""
        return jsonify({'avator': 'avator.jpg', 'login_name': g.user.username, 'user_id': g.user.id, 'user_name': \
                '{0} {1}'.format(g.user.first_name, g.user.last_name), 'first_name': g.user.first_name,
                'user_type': g.user.extinfo.user_type if g.user.extinfo else None, 'api_key': \
                g.user.extinfo.api_key if g.user.extinfo else None, 'last_login': \
                self._format_datetime('%Y-%m-%d %H:%M:%S', g.user.last_login), \
                'last_name': g.user.last_name, 'email': g.user.email, 'access': [role.name for role in g.user.roles]})

    @expose('/logout', methods=['POST'])
    @login_required
    def logout(self):
        """The logout action RESTAPI method."""
        logout_user()
        return jsonify({'msg': 'success'})

    @expose('/reset_mypassword', methods=['POST'])
    @login_required_api
    def reset_mypassword(self):
        """The reset password RESTAPI method."""
        data = request.get_json()
        password = data.get('password')
        if password:
            self.appbuilder.sm.reset_password(g.user.id, password)
            return jsonify({'msg': 'success'})
        else:
            return make_response(jsonify({'msg': 'error parameter'}), 400)

    @expose('/user_list', methods=['GET', 'POST'])
    @has_access_api
    def user_list(self):
        """User list info RESTAPI method."""
        data = request.values
        query = self.appbuilder.get_session.query(MyUser)
        search_obj = data.get('search')
        offset = data.get('offset')
        limit = data.get('limit')
        sort = data.get('sort')
        order = data.get('order')
        if search_obj:
            query = query.filter(or_(MyUser.username.like('%{0}%'.format(search_obj)), \
                                     MyUser.first_name.like('%{0}%'.format(search_obj)), \
                                     MyUser.last_name.like('%{0}%'.format(search_obj))))
        total = query.count()
        #----order
        if sort and order:
            query = query.order_by(text('{0} {1}'.format(sort, order)))
        else:
            query = query.order_by(MyUser.id.asc())
        #----page offset
        if offset and limit:
            query = query.limit(limit)
            query = query.offset(offset)
        records = query.all()
        return jsonify({'rows': [{'id': u.id, 'username': '{0} {1}'.format(u.first_name, u.last_name), \
               'loginname': u.username, 'status': 1 if u.active else 0, 'email': u.email, 'lastlogin': \
               self._format_datetime('%Y-%m-%d %H:%M:%S', u.last_login), 'user_type': u.extinfo.user_type if u.extinfo else None, \
               'roles': [r.name for r in u.roles], 'roles_id': [r.id for r in u.roles], 'extinfo': u.extinfo.to_json() if u.extinfo else None \
               } for u in records], 'total': total})

    @expose('/user_delete', methods=['POST'])
    @has_access_api
    @permission_name('apiUserUpdate')
    def user_delete(self):
        """User delete RESTAPI method."""
        data = request.get_json()
        my_id = data.get('id', None)
        if my_id:
            item = self.datamodel.get(my_id)
            result = self.datamodel.delete(item)
            if result:
                log.debug("user %s successfully been deleted by %s", item.username, g.user.username)
                return jsonify({'msg': "Success deleted user {0}".format(item.username)})
            else:
                return make_response(jsonify({'msg': 'delete failed'}), 500)
        else:
            return make_response(jsonify({'msg': 'user id not exists'}), 400)

    @expose('/user_update', methods=['POST'])
    @has_access_api
    @permission_name('apiUserUpdate')
    def user_update(self):
        """User info update RESTAPI method."""
        data = request.get_json()
        my_id = data.get('id', None)
        if not my_id:
            return make_response(jsonify({'msg': 'Wrong parameter, id is null'}), 400)
        item = self.datamodel.get(my_id)
        if not item:
            return make_response(jsonify({'msg': 'Wrong parameter, user not exists'}), 400)
        roles = self.appbuilder.get_session.query(Role).filter(Role.id.in_(data['rolesSelect'])).all()
        item.roles = roles
        item.active = True if int(data['active']) else False
        if item.extinfo.user_type == 'local':
            item.first_name = data['fn'].strip()
            item.last_name = data['ln'].strip()
            item.username = data['un'].strip()
            item.email = data['email'].strip()
            if data.get('password'):
                item.password = generate_password_hash(data['password'].strip())
        result = self.datamodel.edit(item)
        if result:
            log.debug("Successfully edit user %s by %s", item.username, g.user.username)
            return jsonify({'msg': "Edit user {0} success".format(item.username)})
        else:
            log.error("Failed edit user %s by %s", item.user_name, g.user.username)
            return make_response(jsonify({'msg': "Edit user {0} failed".format(item.username)}), 500)

    @expose('/add_user', methods=['POST'])
    @has_access_api
    @permission_name('apiUserUpdate')
    def user_add(self):
        """add a user method via RESTAPI."""
        data = request.get_json()
        first_name = data['fn'].strip()
        last_name = data['ln'].strip()
        user_name = data['un'].strip().lower()
        password = data['password'].strip()
        email = data['email'].strip()
        # check if user name exists or not
        query = self.appbuilder.get_session.query(func.count('*')).select_from(MyUser).filter(
                    MyUser.username == user_name)
        count = query.scalar()
        if count > 0:
            return jsonify({'msg': 'Login name already exists.'}), 400
        else:
            # fetch role
            roles = self.appbuilder.get_session.query(Role).filter(Role.id.in_(data['rolesSelect'])).all()
            item = MyUser()
            item.extinfo = UserExtInfo(user_type='local')
            item.first_name = first_name
            item.last_name = last_name
            item.username = user_name
            item.active = True if data['active'] else False
            item.email = email
            item.password = generate_password_hash(password)
            item.roles = roles
            result = self.datamodel.add(item)
            if result:
                log.debug("Successfully add user %s by %s", user_name, g.user.username)
                return jsonify({'msg': "Add user {0} success".format(user_name)})
            else:
                log.error("Failed add user %s by %s", user_name, g.user.username)
                return make_response(jsonify({'msg': "Add user {0} failed".format(user_name)}), 500)

    @expose('/self_user_update', methods=['POST'])
    @login_required_api
    def self_user_update(self):
        """self user info update API method."""
        data = request.get_json()
        args = dict()
        for k, v in data.items():
            args[k] = v
        result = self.appbuilder.get_session.query(MyUser).filter_by(id=g.user.id).update(args)
        if result == 1:
            self.appbuilder.get_session.commit()
            return jsonify({'msg': 'success'})
        else:
            return make_response(jsonify({'msg': 'update failed'}), 500)

    @expose('/get_all_users')
    @has_access_api
    def get_all_users(self):
        """Retrieve all user RESTAPI method."""
        return jsonify({'data': [{'first_name': u.first_name, 'last_name': u.last_name, 'username': u.username} \
               for u in self.appbuilder.get_session.query(MyUser.first_name, MyUser.last_name, MyUser.username). \
               select_from(MyUser).all()]})

    @expose('/get_all_roles')
    @has_access_api
    def get_all_roles(self):
        """Retrieve all roles RESTAPI method."""
        return jsonify({'data': [{'id': r.id, 'name': r.name} for r in self.appbuilder.get_session.query(Role).all()]})

    def _format_datetime(self, pattern, date):
        return date.strftime(pattern) if date else None

    @expose('/sync_ldap_user', methods=['POST'])
    @has_access_api
    @permission_name('apiUserUpdate')
    def sync_ldap_user(self):
        data = request.get_json()
        if data.get('coreId'):
            # search user from ldap
            con = ldap.initialize(self.appbuilder.sm.auth_ldap_server)
            con.set_option(ldap.OPT_REFERRALS, 0)
            if self.appbuilder.sm.auth_ldap_use_tls:
                try:
                    con.start_tls_s()
                except Exception:
                    log.info(LOGMSG_ERR_SEC_AUTH_LDAP_TLS.format(self.appbuilder.sm.auth_ldap_server))
                    return jsonify({'msg': 'Init LDAP with SSL connection failed'}), 500
            filter_str = ""
            coreIds = data.get('coreId').split("\n")
            for coreId in coreIds:
                filter_str += "({0}={1})".format(self.appbuilder.sm.auth_ldap_uid_field, coreId.strip())
            filter_str = "(|{0})".format(filter_str)
            users = con.search_s(self.appbuilder.sm.auth_ldap_search,
                    ldap.SCOPE_SUBTREE,
                    filter_str,
                    [self.appbuilder.sm.auth_ldap_uid_field,
                     self.appbuilder.sm.auth_ldap_firstname_field,
                     self.appbuilder.sm.auth_ldap_lastname_field,
                     self.appbuilder.sm.auth_ldap_email_field
                    ])
            # fetch roles
            if data.get('rolesSelect') and len(data['rolesSelect']) > 0:
                roles = self.appbuilder.get_session.query(Role).filter(Role.id.in_(data['rolesSelect'])).all()
            else:
                roles = None
            # sync into local
            success_list = []
            for user_ldapinfo in users:
                motGUID = self.appbuilder.sm.ldap_extract(user_ldapinfo[1], self.appbuilder.sm.auth_ldap_uid_field, None)
                local_user = self.datamodel.session.query(MyUser).filter(MyUser.username == motGUID.lower()).one_or_none()
                if not local_user:
                    local_user = MyUser()
                    local_user.username = motGUID.lower()
                    local_user.active = True
                    local_user.extinfo = UserExtInfo(user_type='ldap')
                local_user.first_name = self.appbuilder.sm.ldap_extract(user_ldapinfo[1], \
                                    self.appbuilder.sm.auth_ldap_firstname_field, local_user.first_name)
                local_user.last_name = self.appbuilder.sm.ldap_extract(user_ldapinfo[1], \
                                    self.appbuilder.sm.auth_ldap_lastname_field, local_user.last_name)
                local_user.email = self.appbuilder.sm.ldap_extract(user_ldapinfo[1], \
                                        self.appbuilder.sm.auth_ldap_email_field, local_user.email)
                if roles:
                    local_user.roles = roles
                result = self.datamodel.edit(local_user)
                if result:
                    log.debug("Successfully sync ldap user %s by %s", local_user.username, g.user.username)
                    success_list.append(local_user.username)
                    coreIds.remove(local_user.username)
                else:
                    log.debug("Failed sync ldap user %s by %s", local_user.username, g.user.username)
            return jsonify({'success_list': success_list, 'failed_list': coreIds})
        else:
            return jsonify({'msg': 'Wrong parameter, coreId is null'}), 400

appbuilder.add_view_no_menu(ApiUserView)
