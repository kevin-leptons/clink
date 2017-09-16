from clink.error.http import HttpArgumentError, Http400Error
from clink.iface import ILv0Handler
from clink.com import stamp
from clink.mime import MIME_JSON


@stamp()
class RecvHandler(ILv0Handler):
    '''
    Receive HTTP message, construct an isinstance of Request

    :param clink.Request req:
    :param clink.Response res:
    :param dict env:
    '''

    def handle(self, req, res, env):
        res.status = 200
        res.content_type = MIME_JSON
        res.header = {}

        req.method = env['REQUEST_METHOD'].lower()
        req.path = env['PATH_INFO']
        if len(req.path) > 1 and req.path[-1] == '/':
            req.path = req.path[:len(req.path) - 1]
        req.header = self._parse_header(env)
        req.server_name = env['SERVER_NAME']
        req.server_port = int(env['SERVER_PORT'])
        req.server_protocol = env['SERVER_PROTOCOL']
        req.remote_addr = env['REMOTE_ADDR']
        if req.method in ['post', 'put', 'patch', 'delete']:
            if 'CONTENT_TYPE' in env:
                req.content_type = env['CONTENT_TYPE'].lower()

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
