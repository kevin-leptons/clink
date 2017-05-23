# STEP 1: get clink library
from clink import stamp, mapper, App, AppConf, Controller
from clink.error.http import Http401Error, Http404Error


# STEP 2: get an WSGI server
from wsgiref.simple_server import make_server


# STEP 3: create application configuration and application
conf = AppConf('book-api', 'Hell Corporation', '1st, Hell street')
app = App(conf)


# STEP 4: define component - controllers
# ===[BEGIN] REMOVE BOOKCTL AND ADD ROOTCTL ==================================
@stamp()
@mapper.path('req')
class RootCtl(Controller):
    @mapper.get('info')
    def get_info(self, req, res):
        res.body = {
            'path': req.path,
            'query_str': req.query_str,
            'content_type': req.content_type,
            'content_length': req.content_length,
            'server_name': req.server_name,
            'server_port': req.server_port,
            'server_protocol': req.server_protocol,
            'remote_addr': req.remote_addr,
            'header': req.header,
            'body': req.body,
        }

    @mapper.get('no-content')
    def no_content(self, req, res):
        res.status = 204

    @mapper.get('not-found')
    def not_found(self, req, res):
        raise Http404Error(req, 'Nothing here')

    @mapper.get('no-auth')
    def no_auth(self, req, res):
        raise Http401Error(req, 'Go back. You are alien')
# ===[END] REMOVE BOOKCTL AND ADD ROOTCTL ====================================


# STEP 5: add components to application
app.add_com(RootCtl)


# STEP 6: load components
app.load()


# STEP 7: serve application on WSGI server
address = 'localhost'
port = 8080
print('Prepare API on http://%s:%i/req/info' % (address, port))
httpd = make_server(address, port, app)
httpd.serve_forever()
