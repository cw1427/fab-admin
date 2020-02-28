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

> Front-end env install

fabadmin front-end bepends on VUE IVIEW, so you have to install nodejs with npm to run the front-end code in dev mode.

- install nodejs 12.x

```bash
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
apt-get install nodejs
```

- cd your fabadmin app folder, and install npm packages

for example your temp folder named: fabadmin, after you bring up fabadmin, you will find app/public folder.

```bash
cd ~/sandbox/fabadmin/app/public
npm install
```

> run fabadmin in dev mod

As default we have front-end code point to http://localhost:8080 as the base url, so we can successfully run fabadmin in prod mod as above:  fabadmin run --port 8080
But, if you can't run in localhost domain, or you want to start develop mode, please refer below code:

```python
1. adjust front base url in app/public/config/url.js

const DEV_URL = 'http://<your server ip>:8081/'

2. adjust front config dev server address in app/public/vue.config.js

    devServer: {
        port: 8080,
        *host: '<your server ip>',*
        contentBase: path.join(__dirname, 'dist'),
    }


2. bring up fabadmin backend:

fabadmin run --port 8081

3. compile front-end code as develop mode: run below code in app/public/ folder

npx vue-cli-service serve

```






