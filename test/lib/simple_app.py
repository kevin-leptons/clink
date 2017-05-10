'''
SYNOPSIS

    start_server(port=8080)

DESCRIPTION

    Start server with one route '/book/item'. It return book information.
'''

from wsgiref.simple_server import make_server
from clink import Application, Route, Router


def start(port=8080):
    route = Route('book')

    @route.get('item')
    def get_book_item(req, res):
        res.body = {
            'name': 'The Linux Programing Interface',
            'author': 'Michael Kerrisk'
        }

    router = Router([route])
    app = Application(router)

    httpd = make_server('', port, app)
    httpd.serve_forever()
