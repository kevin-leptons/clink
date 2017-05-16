'''
SYNOPSIS

    start_server(port=8080)

DESCRIPTION

    Start server with one auth route.
'''

from wsgiref.simple_server import make_server
from clink import AuthApp

JWT_KEY = 'jwt-secret-words'


def start(dburl, dbname, port=8080):
    app = AuthApp('auth-app', dburl, dbname, JWT_KEY)

    httpd = make_server('', port, app)
    httpd.serve_forever()
