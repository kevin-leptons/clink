import sys
from os import path
from os.path import realpath, dirname
from wsgiref.simple_server import make_server

from clink import AppConf, AuthConf, MongoConf, Version
from clink import App, ctl

APP_NAME = 'auth-app'
DB_URL = 'mongodb://localhost'
DB_NAME = APP_NAME
ROOT_PWD = '123456'
JWT_KEY = 'jwt-secret-words'
ADDRESS = 'localhost'


def start(root_email, root_email_pwd, root_email_sever, port=8080):
    app_ver = Version(0, 2, 3)
    app_conf = AppConf(APP_NAME, 'MIT', app_ver, 'clink', 'Ha Noi, Viet Nam')
    mongo_conf = MongoConf(DB_URL, DB_NAME)
    auth_conf = AuthConf(
        ROOT_PWD, root_email, root_email_pwd, root_email_sever, 0, JWT_KEY
    )
    app = App(app_conf)
    app.add_prim(mongo_conf, auth_conf)
    app.add_ctls(ctl)
    app.load()

    print('Prepare to start on http://%s:%i' % (ADDRESS, port))
    httpd = make_server(ADDRESS, port, app)
    httpd.serve_forever()
