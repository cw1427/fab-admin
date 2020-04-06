Fab-admin a flask_appbuilder extension basic app skeleton
=================

- Release note
  - v0.2.0 Add timezone-converter addon
  - v0.1.5 remove requirements.txt
  - v0.1.3 add all fab_manager_overwrite moudle into monkey_patch
  - v0.1.2 add confcenter, queue as an addon, adjust their import way by dynimic import for config_base.
  - v0.1.1 add SSE addon and setup Redis sentinel factory method for pure redis mode.


- Build command
  - python setup.py bdist_wheel -r local
  - twine upload

Depends on:
-----------

- flask
- click
- colorama
- flask-sqlalchemy
- flask-login
- flask-openid
- flask-wtform
- flask-Babel
