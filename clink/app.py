import json

from .http_error import HttpError, HttpArgumentError, code_to_str
from .type import Header, Request, Response


class Application():
    middlewares = []

    def __init__(self, router):
        self._router = router

    def __call__(self, env, start_res):
        try:
            # essentital request, contains few information
            # information will be padding during working
            req = self._ess_req(env)

            # routing
            req_handler = self._router.find_route_handler(req)
            req.args = self._parse_args(env['QUERY_STRING'])

            # essentital Response information, contains few information
            # information wil be padding during working
            res_header = Header()
            res = Response(200, res_header, None)

            # execute middlewares
            for middleware in self.middlewares:
                middleware(req, res)

            # handle request
            req_handler(req, res)

            # response
            header = [('Content-Type', 'application/json')]
            start_res(code_to_str(res.status), header)
            if res.body:
                body_str = json.dumps(res.body)
                return [body_str.encode('utf-8')]
            else:
                return []
        except HttpError as e:
            start_res(code_to_str(e.status), [])
            return []
        except HttpArgumentError as e:
            start_res(code_to_str(400), [])
            return []

    def _ess_req(self, env):
        req_method = env['REQUEST_METHOD']
        req_path = env['PATH_INFO']
        req_header = Header()
        try:
            req_body_size = int(env.get('CONTENT_LENGTH', 0))
        except ValueError:
            req_body_size = 0
        req_body = None
        if req_body_size > 0:
            req_body = env['wsgi.input'].read(req_body_size)
        return Request(req_method, req_path, req_header, req_body)

    def _parse_args(self, arg_str):
        args = {}
        if len(arg_str) == 0:
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
