'''
SYNOPSIS

    class RecvHandler

DESCRIPTION

    Receive request HTTP message, initial req and res
'''

from .http_error import HttpArgumentError, Http400Error
from .mime_type import MIME_JSON
from .ihandler import IRecvHandler


class RecvHandler(IRecvHandler):
    def handle(self, req, res, env):
        res.status = 200
        res.content_type = MIME_JSON
        res.header = {}

        req.method = env['REQUEST_METHOD']
        req.path = env['PATH_INFO']
        req.header = self._parse_header(env)
        req.server_name = env['SERVER_NAME']
        req.server_port = int(env['SERVER_PORT'])
        req.server_protocol = env['SERVER_PROTOCOL']
        req.remote_addr = env['REMOTE_ADDR']
        if req.method.lower() not in ['get', 'head', 'option']:
            req.content_type = env['CONTENT_TYPE']
        try:
            req.args = self._parse_args(env['QUERY_STRING'])
        except HttpArgumentError:
            raise Http400Error(req, 'query string is invalid')

        # read all of body message to memory
        req.content_length = 0
        try:
            req.content_length = int(env.get('CONTENT_LENGTH', 0))
        except ValueError:
            pass
        if req.content_length > 0:
            req.body = env['wsgi.input'].read(req.content_length)

    def _parse_args(self, arg_str):
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

    def _parse_header(self, env):
        header = {}
        for key, value in env.items():
            if key[:5] != 'HTTP_':
                continue
            header[key[5:]] = value
        return header
