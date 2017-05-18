'''
SYNOPSIS

    class App
        add_com(com_type)
        load() 
        __call__()

DESCRIPTION

    add_com() add component to application. com_type argument is type
    of component.

    load() create all of components, solve their depedency.

    __call__() is implements of WSGI.
'''

from os import path

from .iface import IWsgi
from .type import Request, Response
from .routing import Router
from .handler import RecvHandler, SendHandler
from .handler import ReqJsonHandler, ReqUrlEncodeHandler, ReqLogHandler
from .handler import ResJsonHandler, ResCorsHandler
from .handler import ErrorHttpHandler, ErrorLogHandler
from clink.com.injector import Injector, CLINK_COM_ATTR
from clink.type.com import Controller
from clink.routing import Route
from clink.type.com import AppErrHandler, AppReqHandler, AppResHandler


class App(IWsgi):
    req_log_handler = None
    err_log_handler = None

    err_handlers = None
    req_handlers = None
    res_handlers = None

    def __init__(self, conf):
        self.router = Router()
        self.injector = Injector()
        self.injector.add_isnt(conf)

        self.add_com(RecvHandler)
        self.add_com(SendHandler)

        self.add_com(ReqLogHandler)
        self.add_com(ErrorLogHandler)
        self.add_com(ErrorHttpHandler)

        self.add_com(ReqJsonHandler)
        self.add_com(ReqUrlEncodeHandler)
        self.add_com(ResJsonHandler)
        self.add_com(ResCorsHandler)

    def add_com(self, com_type):
        self.injector.add_com(com_type)

    def load(self):
        self.injector.load()
        self._init_routes()

        self.recv_handler = self.injector.instance(RecvHandler)
        self.send_handler = self.injector.instance(SendHandler)
        self.req_log_handler = self.injector.instance(ReqLogHandler)
        self.err_log_handler = self.injector.instance(ErrorLogHandler)

        self.err_handlers = self.injector.instanceof(AppErrHandler)
        self.req_handlers = self.injector.instanceof(AppReqHandler)
        self.res_handlers = self.injector.instanceof(AppResHandler)

    def __call__(self, wsgi_env, wsgi_send):
        req = Request()
        res = Response()

        try:
            # receive message, initial req and res
            self.recv_handler.handle(req, res, wsgi_env)

            # perform request logging handler
            self.req_log_handler.handle(req, res)

            # routing, find main handler
            m_req_handle = self.router.find_handle(req)

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

    def _init_routes(self):
        for type, obj in self.injector.com_inst.items():
            if isinstance(obj, Controller):
                self._add_ctl(obj)

    def _add_ctl(self, ctl):
        base_path = getattr(ctl, CLINK_COM_ATTR)['route_path']
        route = Route(base_path)

        for m in dir(ctl):
            mm = getattr(ctl, m)
            if CLINK_COM_ATTR in dir(mm):
                mm_attrs = getattr(mm, CLINK_COM_ATTR)
                if 'raw_route' not in mm_attrs:
                    continue
                raw_route = mm_attrs['raw_route']
                method = raw_route[0]
                path = raw_route[1]
                req_type = raw_route[2]
                route.add_spec(method, path, req_type, mm)

        self.router.add_route(route)
