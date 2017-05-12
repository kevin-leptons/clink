'''
SYNOPSIS

    class Application

DESCRIPTION

    Implement application with WSGI interface.
'''

from os import path

from .iface import IWsgi
from .type import Request, Response
from .handler import RecvHandler, SendHandler
from .handler import ReqJsonHandler, ReqUrlEncodeHandler, ReqLogHandler
from .handler import ResJsonHandler, ResCorsHandler
from .handler import ErrorHttpHandler, ErrorLogHandler


class Application(IWsgi):
    req_log_handler = None
    err_log_handler = None

    err_handlers = None
    req_handlers = None
    res_handlers = None

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
        self.req_handlers = [ReqJsonHandler(), ReqUrlEncodeHandler()]
        self.res_handlers = [ResJsonHandler(), ResCorsHandler()]

    def __call__(self, wsgi_env, wsgi_send):
        req = Request()
        res = Response()

        try:
            # receive message, initial req and res
            self.recv_handler.handle(req, res, wsgi_env)

            # perform request logging handler
            self.req_log_handler.handle(req, res)

            # routing, find main handler
            m_req_handle = self._router.find_handle(req)

            # perform request handlers
            for handler in self.req_handlers:
                handler.handle(req, res)

            # perform main handler
            m_req_handle(req, res)

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

            # perform error logging handler
            self.err_log_handler.handle(req, res, e)

            # send error response
            return self.send_handler.handle(req, res, wsgi_send)
