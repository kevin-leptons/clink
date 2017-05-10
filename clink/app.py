from .http_error import code_to_str
from .type import Request, Response
from .recv_handler import recv_handler
from .send_handler import send_handler
from .req_handler import json_req_handle, form_req_handle
from .res_handler import json_res_handle, cors_res_handle
from .err_handler import http_err_handler


class Application():
    recv_handler = staticmethod(recv_handler)  # fn(req, res, wsgi_env)
    send_handler = staticmethod(send_handler)  # fn(req, res, wsig_send)

    req_handlers = [json_req_handle, form_req_handle]  # fn(req, res)
    res_handlers = [json_res_handle, cors_res_handle]  # fn(req, res)

    err_handlers = [http_err_handler]  # fn(req, res, e)

    def __init__(self, router):
        self._router = router

    def __call__(self, wsgi_env, wsgi_send):
        req = Request()
        res = Response()
        res.status = 200
        res.content_type = 'application/json'
        res.header = {}

        try:
            # receive message
            self.recv_handler(req, res, wsgi_env)

            # perform request handlers
            for handler in self.req_handlers:
                handler(req, res)

            # routing and perform controller
            ctl_handler = self._router.find_route_handler(req)
            ctl_handler(req, res)

            # perform response handlers
            for handler in self.res_handlers:
                handler(req, res)

            # send response
            self.send_handler(req, res, wsgi_send)
            if res.body is None:
                return []
            else:
                return [res.body.encode('utf-8')]

            # header = [('Content-Type', 'application/json')]
            # wsgi_send('200 OK', header)
            # return ['123'.encode('utf-8')]
        except Exception as e:
            # if error handlers raise error, it's handlers by server
            # which runs this application
            for handler in self.err_handlers:
                handler(req, res, e, wsgi_send)
            header = [('Content-Type', 'application/json')]
            wsgi_send(code_to_str(res.status), header)
            if res.body is None:
                return []
            else:
                return [res.body.encode('utf-8')]
