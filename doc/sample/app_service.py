# STEP 1: get clink library
from clink import stamp, mapper, App, AppConf, Controller, Service
from clink.mime.type import MIME_PLAINTEXT
from bson import ObjectId


# STEP 2: get an WSGI server
from wsgiref.simple_server import make_server


# STEP 3: create application configuration and application
conf = AppConf('book-api', 'Hell Corporation', '1st, Hell street')
app = App(conf)


# STEP 4: define components
# ===[BEGIN] DEFINE SERVICES =================================================
@stamp(AppConf)
class PubService(Service):
    def __init__(self, app_conf):
        self._app_conf = app_conf

    def publish(self, type, content):
        id = ObjectId()
        parts = (
            'Id: ', str(id), '\n',
            'Type: ', type, '\n',
            'Content:\n\n', content, '\n\n',
            self._app_conf.name, '\n',
            self._app_conf.org_name, '\n',
            self._app_conf.org_loc,
        )
        return ''.join(parts)


@stamp(PubService)
@mapper.path('newsparer')
class NewsCtl(Controller):
    def __init__(self, pub_sv):
        self._pub_sv = pub_sv

    @mapper.post('', MIME_PLAINTEXT)
    def publish(self, req, res):
        content = req.body.decode('utf-8')
        pub = self._pub_sv.publish('NEWSPAPER', content)
        res.body = pub.encode('utf-8')
        res.content_type = MIME_PLAINTEXT


@stamp(PubService)
@mapper.path('magazine')
class MagazineCtl(Controller):
    def __init__(self, pub_sv):
        self._pub_sv = pub_sv

    @mapper.post('', MIME_PLAINTEXT)
    def publish(self, req, res):
        content = req.body.decode('utf-8')
        pub = self._pub_sv.publish('MAGAZINE', content)
        res.body = pub.encode('utf-8')
        res.content_type = MIME_PLAINTEXT

# ===[END] DEFINE SERVICES ===================================================


# STEP 5: add components to application
app.add_ctl(NewsCtl)
app.add_ctl(MagazineCtl)

# STEP 6: load components
app.load()

# STEP 7: serve application on WSGI server
address = 'localhost'
port = 8080
print('Prepare API on http://%s:%i' % (address, port))
httpd = make_server(address, port, app)
httpd.serve_forever()
