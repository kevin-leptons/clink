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

    Handler MUST follow description blow:

        Lv0Handler: Receive HTTP message Handling
        Lv1Handler: Pre-Routing Handling
        Lv2Handler: Routing Handling
        Lv3Handler: Pre-Main Handling
        Lv4Handler: Main Handling
        Lv5Handler: Responding Handling
        Lv6Handler: Sending Handling
        Lv7Handler: Error Handling
        Lv8Handler: Error Logging Handling
        Lv9Handler: Error Sending Handling
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
from clink.routing import Route
from clink.type import *


class App(IWsgi):
    lv0_handler = None
    lv1_handler = None
    lv3_handlers = None
    lv5_handlers = None
    lv6_handler = None
    lv7_handlers = None
    lv8_handler = None
    lv9_handler = None

    def __init__(self, conf):
        self.router = Router()
        self.injector = Injector()
        self.injector.add_inst(conf)

        self.add_com(RecvHandler)
        self.add_com(ReqLogHandler)
        self.add_com(ReqJsonHandler)
        self.add_com(ReqUrlEncodeHandler)
        self.add_com(ResJsonHandler)
        self.add_com(ResCorsHandler)
        self.add_com(SendHandler)
        self.add_com(ErrorHttpHandler)
        self.add_com(ErrorLogHandler)

    def add_com(self, com_type):
        self.injector.add_com(com_type)

    def load(self):
        self.injector.load()
        self._init_routes()

        self.lv0_handler = self.injector.instanceof(Lv0Handler)[0]
        self.lv1_handler = self.injector.instanceof(Lv1Handler)[0]
        self.lv3_handlers = self.injector.instanceof(Lv3Handler)
        self.lv5_handlers = self.injector.instanceof(Lv5Handler)
        self.lv6_handler = self.injector.instanceof(Lv6Handler)[0]
        self.lv7_handlers = self.injector.instanceof(Lv7Handler)
        self.lv8_handler = self.injector.instanceof(Lv8Handler)[0]
        self.lv9_handler = self.lv6_handler

    def __call__(self, wsgi_env, wsgi_send):
        # level 0: recv handling
        req = Request()
        res = Response()

        try:
            # level 0 continue: receiving handling
            self.lv0_handler.handle(req, res, wsgi_env)

            # level 1: pre-routing handling
            self.lv1_handler.handle(req, res)

            # level 2: routing, find main handler
            lv4_handle = self.router.find_handle(req)

            # level 3: pre-main handling
            for handler in self.lv3_handlers:
                handler.handle(req, res)

            # level 4: main handling
            lv4_handle(req, res)

            # level 5: response handling
            for handler in self.lv5_handlers:
                handler.handle(req, res)

            # level 6: send handling
            return self.lv6_handler.handle(req, res, wsgi_send)
        except Exception as e:
            # level 7: error handling
            handled = False
            for handler in self.lv7_handlers:
                if handler.handle(req, res, e):
                    handled = True
            if not handled:
                raise e

            # level 8: error log handling
            self.lv8_handler.handle(req, res, e)

            # level 9: send error response
            return self.lv9_handler.handle(req, res, wsgi_send)

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
