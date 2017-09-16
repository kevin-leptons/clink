from wsgiref.simple_server import make_server
from clink import stamp, mapper, App, AppConf, Controller
from clink.error.http import Http400Error, Http401Error, Http403Error,\
                             Http404Error, Http405Error, Http409Error,\
                             Http500Error
from clink.mime import MIME_PLAINTEXT


@stamp()
@mapper.path('/')
class RootCtl(Controller):
    @mapper.get('/')
    def api_info(self, req, res):
        res.body = {
            'header': req.header,
            'path': req.path,
            'args': req.args,
            'server_name': req.server_name,
            'server_port': req.server_port,
            'server_protocol': req.server_protocol,
            'content_length': req.content_length
        }


@stamp()
@mapper.path('/res')
class ResourceCtl(Controller):
    @mapper.get('/item')
    def get_item(self, req, res):
        pass

    @mapper.post('/item')
    def post_item(self, req, res):
        pass

    @mapper.put('/item')
    def put_item(self, req, res):
        pass

    @mapper.patch('/item')
    def patch_item(self, req, res):
        pass

    @mapper.delete('/item')
    def delete_item(self, req, res):
        pass

    @mapper.get('/get')
    def get_only(self, req, res):
        pass

    @mapper.post('/post')
    def post_only(self, req, res):
        pass

    @mapper.put('/put')
    def put_only(self, req, res):
        pass

    @mapper.patch('/patch')
    def patch_only(self, req, res):
        pass

    @mapper.delete('/delete')
    def delete_only(self, req, res):
        pass

    @mapper.post('/text', MIME_PLAINTEXT)
    def post_text(self, req, res):
        pass


@stamp()
@mapper.path('/status')
class StatusCtl(Controller):
    @mapper.get('/400')
    def http400(self, req, res):
        raise Http400Error(req)

    @mapper.get('/401')
    def http401(self, req, res):
        raise Http401Error(req)

    @mapper.get('/403')
    def http403(self, req, res):
        raise Http403Error(req)

    @mapper.get('/404')
    def http404(self, req, res):
        raise Http404Error(req)

    @mapper.get('/405')
    def http405(self, req, res):
        raise Http405Error(req)

    @mapper.get('/409')
    def http409(self, req, res):
        raise Http409Error(req)

    @mapper.get('/500')
    def http500(self, req, res):
        raise Http500Error(req)


def start(port=8080):
    app_conf = AppConf('simple-api')
    app = App(app_conf)
    app.add_ctl(RootCtl)
    app.add_ctl(StatusCtl)
    app.add_ctl(ResourceCtl)
    app.load()

    httpd = make_server('localhost', port, app)
    httpd.serve_forever()
