import sys
from os import path
from os.path import realpath, dirname
from wsgiref.simple_server import make_server
from pymongo import MongoClient

from clink import AppConf, AuthConf, MongoConf, Version
from clink import App, ctl, stamp, mapper, Controller
from clink.service import OAuthSv

APP_NAME = 'auth-app'
DB_URL = 'mongodb://localhost'
DB_NAME = APP_NAME
JWT_KEY = 'jwt-secret-words'
ADDRESS = 'localhost'


@stamp(OAuthSv)
@mapper.path('/res')
class ResourceApi(Controller):
    def __init__(self, oauth_sv):
        self._oauth_sv = oauth_sv

    @mapper.get('/item')
    def get_item(self, req, res):
        acc_id = self._oauth_sv.authen_req(req)
        res.body = {
            'account_id': acc_id
        }


def start(root_pwd, root_email, root_email_pwd, root_email_sever, 
          root_email_server_port, port=8080):

    app_ver = Version(0, 2, 3)
    app_conf = AppConf(APP_NAME, 'MIT', app_ver, 'clink', 'Ha Noi, Viet Nam')
    mongo_conf = MongoConf(DB_URL, DB_NAME)
    auth_conf = AuthConf(
        root_pwd, root_email, root_email_pwd, root_email_sever, 0, JWT_KEY
    )

    mongo_client = MongoClient(mongo_conf.dburl)
    mongo_client.drop_database(mongo_conf.dbname)
    mongo_client.close()

    app = App(app_conf)
    app.add_prim(mongo_conf, auth_conf)
    app.add_ctls(ctl)
    app.add_ctl(ResourceApi)
    app.load()

    print('Prepare to start on http://%s:%i' % (ADDRESS, port))
    httpd = make_server(ADDRESS, port, app)
    httpd.serve_forever()
