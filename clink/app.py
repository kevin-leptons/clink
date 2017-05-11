from .type import Request, Response
from .recv_handler import recv_handler
from .send_handler import send_handler
from .req_handler import json_req_handle, form_req_handle
from .res_handler import json_res_handle, cors_res_handle
from .err_handler import http_err_handler


class Application():
    recv_handler = staticmethod(recv_handler)  # fn(req, res, wsgi_env)
    send_handler = staticmethod(send_handler)  # fn(req, res, wsgi_send)

    p_req_handlers = []  # fn(req, res)
    n_req_handlers = [json_req_handle, form_req_handle]  # fn(req, res)
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

            # perform prev request handlers
            for handler in self.p_req_handlers:
                handler(req, res)

            # routing
            m_req_handler = self._router.find_route_handler(req)

            # perfrom next request handlers
            for handler in self.n_req_handlers:
                handler(req, res)

            # perform main request handler
            m_req_handler(req, res)

            # perform response handlers
            for handler in self.res_handlers:
                handler(req, res)
        except Exception as e:
            # if error handlers raise error, it's handlers by server
            # which runs this application
            for handler in self.err_handlers:
                handler(req, res, e, wsgi_send)

        # send response
        # if sending cause error, it's handlers by Server
        # which runs this application
        return send_handler(req, res, wsgi_send)

        # header = [('Content-Type', 'application/json')]
        # wsgi_send('200 OK', header)
        # return ['123'.encode('utf-8')]
