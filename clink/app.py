from .type import Request, Response
from .recv_handler import recv_handle
from .send_handler import send_handle
from .req_handler import json_req_handle, urlencode_req_handle
from .req_log_handler import log_req_handle
from .res_handler import json_res_handle, cors_res_handle
from .res_log_handler import log_res_handle
from .err_handler import http_err_handle
from .err_log_handler import log_err_handle


class Application():
    recv_handle = staticmethod(recv_handle)  # fn(req, res, wsgi_env)
    send_handle = staticmethod(send_handle)  # fn(req, res, wsgi_send)

    p_req_handlers = [log_req_handle]  # fn(req, res)
    n_req_handlers = [json_req_handle, urlencode_req_handle]  # fn(req, res)
    res_handlers = [
        json_res_handle, cors_res_handle, log_res_handle
    ]  # fn(req, res)

    err_handlers = [http_err_handle, log_err_handle]  # fn(req, res, e)

    def __init__(self, router):
        self._router = router

    def __call__(self, wsgi_env, wsgi_send):
        req = Request()
        res = Response()

        try:
            # receive message
            self.recv_handle(req, res, wsgi_env)

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

            # send response
            return send_handle(req, res, wsgi_send)
        except Exception as e:
            # if error handlers raise error, it's handlers by server
            # which runs this application
            handled = False
            for handler in self.err_handlers:
                if handler(req, res, e):
                    handled = True
            if not handled:
                raise e

            # send error response
            return send_handle(req, res, wsgi_send)
