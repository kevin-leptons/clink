'''
SYNOPSIS

    start_server(port=8080)

DESCRIPTION

    Start server with one route '/book/item'. It return book information.
'''

from wsgiref.simple_server import make_server
from clink import Application, Route, Router


def start(port=8080):
    route = Route('api')

    @route.get('info')
    def get_book_item(req, res):
        res.body = {
            'header': req.header,
            'path': req.path,
            'args': req.args,
            'server_name': req.server_name,
            'server_port': req.server_port,
            'server_protocol': req.server_protocol,
            'content_type': req.content_type,
            'content_length': req.content_length
        }

    router = Router([route])
    app = Application(router)

    httpd = make_server('', port, app)
    httpd.serve_forever()
