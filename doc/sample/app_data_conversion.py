# STEP 1: get clink library
from clink import App, AppConf, com, route, Controller
from clink import Lv3Handler, Lv5Handler
from clink.mime.type import MIME_PLAINTEXT

# STEP 2: get an WSGI server
from wsgiref.simple_server import make_server

# STEP 3: create application configuration and application
conf = AppConf('book-api', 'Hell Corporation', '1st, Hell street')
app = App(conf)

# STEP 4: define component - controllers
#===[BEGIN] ADD DATA CONVERSION HANDLERS =====================================
@com()
class ReqTextHandler(Lv3Handler):
    def handle(self, req, res):
        if req.content_type != MIME_PLAINTEXT :
            return
        if req.body is None:
            req.body = []
        else:
            req.body = req.body.decode('utf-8').split(' ')

@com()
class ResTextHandler(Lv5Handler):
    def handle(self, req, res):
        if res.content_type != MIME_PLAINTEXT:
            return
        if res.body is None:
            res.body = ''
        else:
            res.body = ' '.join(res.body).encode('utf-8')

@com()
@route.path('text')
class TextCtl(Controller):
    @route.post('', MIME_PLAINTEXT)
    def process_text(self, req, res):
        res.body = [w.upper() for w in req.body]
        res.content_type = MIME_PLAINTEXT
#===[END] ADD DATA CONVERSION HANDLERS =======================================

# STEP 5: add components to application
app.add_com(ReqTextHandler)
app.add_com(ResTextHandler)
app.add_com(TextCtl)

# STEP 6: load components
app.load()

# STEP 7: serve application on WSGI server
address = 'localhost'
port = 8080
print('Prepare API on http://%s:%i/text' % (address, port))
httpd = make_server(address, port, app)
httpd.serve_forever()
