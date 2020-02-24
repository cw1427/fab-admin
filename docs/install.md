# fab_admin v0.1.0


> fab_admin based on [flask_appbuilder](https://github.com/cw1427/Flask-AppBuilder)

fab_admin is one python library based on flask_appbuilder v1.12.3, it brings some extension commands like

 -*fab_admin clone*

> python pip install

You can directly install fab_admin from pypi

> Mysql client library and python dev

 - apt-get install libmysqlclient-dev python-dev

fab_admin depends on mysqlclient when doing pip install, so you have to run the libmysqlclient-dev lib install in os

```linux
apt-get install libmysqlclient-dev python-dev
```

> sqlite3

As default fab-admin would need sqlite3 db to init its data structure, so it needs to be install in linux DB

```bash

apt-get install sqlite3 libsqlite3-dev
```

> use pyenv to reinstall python3.6.8

If you forget to install sqlite3 lib before install python, you have to reinstall python3.

```python
    pyenv install 3.6.8
```

> clone fabadmin basic app

```python

   mkdir test
   cd test
   fabadmin clone -n <you app name e.g: cwtest>:  fabadmin clone -n cwtest
```

> bring fabadmin up

Run below command to bring up a web service based on fabadmin.

access:  http://localhost:8080  you will see the web site.


```python
    fabadmin run --port 8080
```

