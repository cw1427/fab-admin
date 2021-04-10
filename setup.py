import os
import sys
import imp
import multiprocessing
from setuptools import setup, find_packages


version = imp.load_source('version', os.path.join('fab_admin', 'version.py'))

def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)

def read(fname):
    return open(fpath(fname)).read()

def desc():
    return read('README.md')

def gather_package_data(folder_name):
    import glob
    data_files = glob.glob(f"{folder_name}/**", recursive=True)
    hidden_files = glob.glob(f"{folder_name}/**/.*", recursive=True)
    return data_files + hidden_files
#     return (folder_name, data_files + hidden_files)

setup(
    name='fab-admin',
    version=version.VERSION_STRING,
    url='',
    license='BSD',
    author='Shawn Chen',
    author_email='cwvinus@163.com',
    description='',
    long_description=desc(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={'fab_admin.addon': gather_package_data('fab_admin/addon'),
                  'fab_admin.app_templates': gather_package_data('fab_admin/app_templates'),
                  'fab_admin.fab_manager_overwrite': gather_package_data('fab_admin/fab_manager_overwrite')},
#     data_files=[gather_package_data('fab_admin/addon'),gather_package_data('fab_admin/app_templates'),
#                 gather_package_data('fab_admin/fab_manager_overwrite')],
    entry_points={'console_scripts': [
          'fabadmin = fab_admin.console:cli',
      ]},
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        "colorama==0.3.9",
        "click==6.7",
        "SQLAlchemy==1.3.0",
        "Flask>=0.12.1,<0.12.99",
        "Jinja2>=2.8",
        "Flask-Login==0.4.1",
        "Flask-SQLAlchemy==2.3",
        "Flask-OpenID==1.2.5",
        "Flask-WTF==0.14.2",
        "Flask-Babel==0.12.2",
        "Flask-AppBuilder==1.12.3",
        "Flask-Session==0.3.1",
        "Flask-Cors==3.0.7",
        "fab-addon-autodoc>=0.1.5",
        "python-ldap==3.2.0",
        "mysqlclient==1.4.2",
        "pyMySQL==0.9.3",
        "gevent==1.4.0",
        "Flask-Redis==0.3.0",
        "redis==3.2.1",
        "hiredis==1.0.0",
        "rejson==0.4.0",
        "graphene>=2.1",
        "graphene-sqlalchemy==2.1.0",
        "Flask-GraphQL==2.0.0",
        "requests==2.20.0",
        "virtualenv==16.4.3",
        # "uwsgi==2.0.18",
        # "uwsgi-tasks==0.7.2",
        "Flask-Redis-Sentinel==2.0.1",
        "Flask-RQ2==18.3",
        "rq==1.0",
        "rq-dashboard==0.5.1",
        "rq-scheduler==0.9",
        "rq-scheduler-dashboard==0.0.2",
        "Flask-CLI==0.4.0",
        "supervisor==4.0.3",
        "flask-emails==0.4.2"
    ],
    tests_require=[
        'nose>=1.0'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='nose.collector'
)
