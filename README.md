Fab-admin a flask_appbuilder app skeleton
=========================================

 Quick start:
 ------------

- pip install fab_admin
- Init step
  - 1. cd to a empty folder
  - 2. fab_admin clone
  - 3. fab_admin run --port 8080




- Features
 - Front-end based on VUE IVIEW
 - Redis
 - RQ
 - Schedule
 - SSE
 - GraphQL
 - Mail
 - Addon

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

Deploy and install:

- python setup.py sdist --formats=gztar,zip

- Make it Public::

  - python setup.py sdist upload -r pypi
  - twine upload pypi
