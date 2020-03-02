# Install

fab-admin based on python version >= 3.6.8

## Install fab-admin

> Befor install

fab-admin has dev, test and prod 3 kinds of execute mode. As default, it runs in dev and with sqlite3 dependency.
for test and prod mode, it needs mysqlclient to integrate with mysql. So it is better to prepare those module in your OS.

 - sqlite3

```linux
apt-get install sqlite3 libsqlite3-dev
```

 -  Mysql client library and python dev

```linux
apt-get install libmysqlclient-dev python-dev
```


 - use pyenv to reinstall python3.6.8

 If you forget to install sqlite3 lib before install python, you have to reinstall python3.

```python
    pyenv install 3.6.8
```


> install fab-admin from pypi

You can directly install fab_admin from pypi

```python
pip install fab-admin
```

## Init app

Once we have successfully install fab-admin (all of the dependencies have been installed), we can use start init your app.

### Check install

Prepare a empty folder, we can cd into it and run the fabadmin to check if it had been installed successfully:

```linux
(env3_6_8) ****@***:~/sandbox/cwtest$ fabadmin
```

Below are a part of the output
```linux
[2020-03-02 22:03:39,919] INFO 6723 [flask_appbuilder.security.sqla.manager] manager.py:384 - [shws4] - Added Permission menu access on AutoDocumentsView to role Admin
[2020-03-02 22:03:39,919] INFO 6723 [flask_appbuilder.base] base.py:276 - [shws4] - Registered AddOn: fab_addon_autodoc.manager.AutoDocManager
WARNING: Was unable to import app Error: No module named 'app'
There is no extend commands import Error: No module named 'app'
Usage: fabadmin [OPTIONS] COMMAND [ARGS]...

  A fabmanager CLI extension, to bring some useful command for fab_admin app
  clone

Options:
  --help  Show this message and exit.

Commands:
  babel-compile     Babel, Compiles all translations
  babel-extract     Babel, Extracts and updates all messages...
  clone             Clone a basic fab_admin app
  collect-static    Copies flask-appbuilder static files to your...
  create-addon      Create a Skeleton AddOn (needs internet...
  create-admin      Creates an admin user
  create-app        Create a Skeleton application (needs internet...
  create-db         Create all your database objects (SQLAlchemy...
  create-user       Create a user
  list-users        List all users on the database
  list-views        List all registered views
  reset-password    Resets a user's password
  run               Runs Flask dev web server.
  security-cleanup  Cleanup unused permissions from views and...
  ssehb             The heart beat command to check the invalid...
  syncauth          Try to sync fab auth structure data into...
  version           Flask-AppBuilder package version

```

### Clone fabadmin basic app

We will see a list of commands above, there is one command: fab-admin clone. As default it will help to initialize an app

As default fabadmin has the compiled front-end code with:  localhost as the backend address. So if you do the trial on your
localhost, you can directly bring it without recompile the front-end code.

### Trial in the localhost

 - Step 1: Clone an app with your app_name as below:
 
```linux
   fabadmin clone -n cwtest
```

 - Step 2: Bring fabadmin up
 
```python
    fabadmin run --port 8080
```

 - Step 3:  Access http://localhost:8080  you will see the web site.

![Login page](./img/fab_login_page.jpg)

 - Step 4: Create a admin account
 
 We can use fabadmin built-in command to generate one admin account.
 Please run the command in the root path of your folder.

```linux
$ fabadmin create-admin
Username [admin]:
User first name [admin]:
User last name [user]:
Email [admin@fab.org]:
Password:
Repeat for confirmation:
Recognized LDAP Authentication.
Admin User admin created.
```
 After your admin account created, you can successfully login your app.
![Login page](./img/fab_home_page.jpg)
 


## Front-end env install

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






