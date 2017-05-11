from os import path

from .type import Request, Response
from .recv_handler import RecvHandler
from .send_handler import SendHandler
from .req_json_handler import ReqJsonHandler
from .req_urlenc_handler import ReqUrlEncHandler
from .req_log_handler import ReqLogHandler
from .res_json_handler import ResJsonHandler
from .res_cors_handler import ResCorsHandler
from .err_http_handler import ErrorHttpHandler
from .err_log_handler import ErrorLogHandler


class Application():
    req_log_handler = None
    err_log_handler = None

    req_handlers = None
    res_handlers = None
    err_handlers = None

    def __init__(self, name, router):
        self._name = name
        self._router = router

        self.recv_handler = RecvHandler()
        self.send_handler = SendHandler()

        req_logfile = path.join('/var/tmp', name, 'request.log')
        self.req_log_handler = ReqLogHandler(req_logfile)

        err_logfile = path.join('/var/tmp', name, 'error.log')
        self.err_log_handler = ErrorLogHandler(err_logfile)

        self.err_handlers = [ErrorHttpHandler()]
        self.req_handlers = [ReqJsonHandler(), ReqUrlEncHandler()]
        self.res_handlers = [ResJsonHandler(), ResCorsHandler()]

    def __call__(self, wsgi_env, wsgi_send):
        req = Request()
        res = Response()

        try:
            # receive message, initial req and res
            self.recv_handler.handle(req, res, wsgi_env)

            # perform request logging handler
            self.req_log_handler.handle(req, res)

            # perform request handlers
            for handler in self.req_handlers:
                handler.handle(req, res)

            # routing, find main handler and perform it
            m_req_handler = self._router.find_route_handler(req)
            m_req_handler(req, res)

            # perform response handlers
            for handler in self.res_handlers:
                handler.handle(req, res)

            # send response
            return self.send_handler.handle(req, res, wsgi_send)
        except Exception as e:
            # perform error handlers
            handled = False
            for handler in self.err_handlers:
                if handler.handle(req, res, e):
                    handled = True
            if not handled:
                raise e

            # send error response
            return self.send_handler.handle(req, res, wsgi_send)

            # perform error logging handler
            self.err_log_handler.handle(req, res, e)
