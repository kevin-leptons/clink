# STEP 1: get clink library
from clink import stamp, mapper, App, AppConf, Controller
from clink.iface import ILv3Handler, ILv5Handler
from clink.mime.type import MIME_PLAINTEXT


# STEP 2: get an WSGI server
from wsgiref.simple_server import make_server


# STEP 3: create application configuration and application
conf = AppConf('book-api', 'Hell Corporation', '1st, Hell street')
app = App(conf)


# STEP 4: define components
# ===[BEGIN] ADD DATA CONVERSION HANDLERS ====================================
@stamp()
class ReqTextHandler(ILv3Handler):
    def handle(self, req, res):
        if req.content_type != MIME_PLAINTEXT:
            return
        if req.body is None:
            req.body = []
        else:
            req.body = req.body.decode('utf-8').split(' ')


@stamp()
class ResTextHandler(ILv5Handler):
    def handle(self, req, res):
        if res.content_type != MIME_PLAINTEXT:
            return
        if res.body is None:
            res.body = ''
        else:
            res.body = ' '.join(res.body).encode('utf-8')


@stamp()
@mapper.path('/text')
class TextCtl(Controller):
    @mapper.post('/', MIME_PLAINTEXT)
    def process_text(self, req, res):
        res.body = [w.upper() for w in req.body]
        res.content_type = MIME_PLAINTEXT
# ===[END] ADD DATA CONVERSION HANDLERS ======================================


# STEP 5: add components to application
app.add_handler(ReqTextHandler)
app.add_handler(ResTextHandler)
app.add_ctl(TextCtl)

# STEP 6: load components
app.load()

# STEP 7: serve application on WSGI server
address = 'localhost'
port = 8080
print('Prepare API on http://%s:%i/text' % (address, port))
httpd = make_server(address, port, app)
httpd.serve_forever()
