from wsgiref.simple_server import make_server
from clink import stamp, mapper, App, AppConf, Controller


@stamp()
@mapper.path('api')
class BookCtl(Controller):
    @mapper.get('info')
    def get_book_item(self, req, res):
        res.body = {
            'header': req.header,
            'path': req.path,
            'args': req.args,
            'server_name': req.server_name,
            'server_port': req.server_port,
            'server_protocol': req.server_protocol,
            'content_length': req.content_length
        }


def start(port=8080):
    app_conf = AppConf('simple-api')
    app = App(app_conf)
    app.add_com(BookCtl)
    app.load()

    httpd = make_server('localhost', port, app)
    httpd.serve_forever()
