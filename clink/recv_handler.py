'''
SYNOPSIS

    recv_handler(req, res, wsgi_env)

DESCRIPTION

    Receive request HTTP message, parse information into object
'''

from .http_error import HttpArgumentError, Http400Error
from .mime_type import MIME_JSON


def recv_handle(req, res, wsgi_env):
    res.status = 200
    res.content_type = MIME_JSON
    res.header = {}

    req.method = wsgi_env['REQUEST_METHOD']
    req.path = wsgi_env['PATH_INFO']
    req.header = _parse_header(wsgi_env)
    req.server_name = wsgi_env['SERVER_NAME']
    req.server_port = int(wsgi_env['SERVER_PORT'])
    req.server_protocol = wsgi_env['SERVER_PROTOCOL']
    req.content_type = wsgi_env['CONTENT_TYPE']
    req.remote_addr = wsgi_env['REMOTE_ADDR']
    try:
        req.args = _parse_args(wsgi_env['QUERY_STRING'])
    except HttpArgumentError:
        raise Http400Error(req, 'query string is invalid')

    # read all of body message to memory
    req.content_length = 0
    try:
        req.content_length = int(wsgi_env.get('CONTENT_LENGTH', 0))
    except ValueError:
        pass
    if req.content_length > 0:
        req.body = wsgi_env['wsgi.input'].read(req.content_length)


def _parse_args(arg_str):
    args = {}
    if arg_str is None or len(arg_str) == 0:
        return args
    arg_coms = arg_str.split('&')
    for arg_com in arg_coms:
        arg_parts = arg_com.split('=')
        if len(arg_parts) != 2:
            raise HttpArgumentError(arg_str)
        if len(arg_parts[0]) == 0 or len(arg_parts[1]) == 0:
            raise HttpArgumentError(arg_str)
        args[arg_parts[0]] = arg_parts[1]
    return args


def _parse_header(wsgi_env):
    header = {}
    for key, value in wsgi_env.items():
        if key[:5] != 'HTTP_':
            continue
        header[key[5:]] = value
    return header
