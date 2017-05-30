import sys
from os import path
from os.path import realpath, dirname
from wsgiref.simple_server import make_server

from clink import AppConf, AuthConf, MongoConf, Version
from clink import App, ctl

_TMP_DIR = realpath(path.join(dirname(__file__), '../../tmp'))
sys.path.append(_TMP_DIR)

from test_conf import ROOT_EMAIL, ROOT_EMAIL_PWD, ROOT_EMAIL_SERVER

APP_NAME = 'auth-app'
DB_URL = 'mongodb://localhost'
DB_NAME = APP_NAME
ROOT_PWD = '123456'
JWT_KEY = 'jwt-secret-words'
ADDRESS = '0'


def start(port=8080):
    app_ver = Version(0, 2, 3)
    app_conf = AppConf(APP_NAME, 'MIT', app_ver, 'clink', 'Ha Noi, Viet Nam')
    mongo_conf = MongoConf(DB_URL, DB_NAME)
    auth_conf = AuthConf(
        ROOT_PWD, ROOT_EMAIL, ROOT_EMAIL_PWD, ROOT_EMAIL_SERVER, JWT_KEY
    )
    app = App(app_conf)
    app.add_prim(mongo_conf, auth_conf)
    app.add_ctls(ctl)
    app.load()

    print('Prepare to start on http://%s:%i' % (ADDRESS, port))
    httpd = make_server(ADDRESS, port, app)
    httpd.serve_forever()
