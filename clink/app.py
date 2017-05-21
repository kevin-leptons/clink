from os import path

from .iface import IWsgi
from .type import Request, Response
from .routing import Router
from .handler import RecvHandler, SendHandler
from .handler import ReqJsonHandler, ReqUrlEncodeHandler, ReqLogHandler
from .handler import ResJsonHandler, ResCorsHandler
from .handler import ErrorHttpHandler, ErrorLogHandler
from clink.com.injector import Injector
from clink.com.type import COM_ATTR
from clink.routing import Route
from clink.type import *


class App(IWsgi):
    '''
    Application brings APIs to HTTP
    '''

    _lv0_handler = None
    _lv1_handler = None
    _lv3_handlers = None
    _lv5_handlers = None
    _lv6_handler = None
    _lv7_handlers = None
    _lv8_handler = None
    _lv9_handler = None

    def __init__(self, conf):
        '''
        Create application from essential configuration

        :param clink.AppConf conf:
        '''

        self.router = Router()
        self.injector = Injector()
        self.injector.add_ref(conf)

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
        '''
        Add a component to application

        :param class com_type:
        '''

        self.injector.add_com(com_type)

    def load(self):
        '''
        Creeate instance of all of components, put it to ready state
        '''

        self.injector.load()
        self._init_routes()

        self._lv0_handler = self.injector.sub_ref(Lv0Handler)[0]
        self._lv1_handler = self.injector.sub_ref(Lv1Handler)[0]
        self._lv3_handlers = self.injector.sub_ref(Lv3Handler)
        self._lv5_handlers = self.injector.sub_ref(Lv5Handler)
        self._lv6_handler = self.injector.sub_ref(Lv6Handler)[0]
        self._lv7_handlers = self.injector.sub_ref(Lv7Handler)
        self._lv8_handler = self.injector.sub_ref(Lv8Handler)[0]
        self._lv9_handler = self._lv6_handler

    def __call__(self, wsgi_env, wsgi_send):
        # level 0: recv handling
        req = Request()
        res = Response()

        try:
            # level 0 continue: receiving handling
            self._lv0_handler.handle(req, res, wsgi_env)

            # level 1: pre-routing handling
            self._lv1_handler.handle(req, res)

            # level 2: routing, find main handler
            lv4_handle = self.router.find_handle(req)

            # level 3: pre-main handling
            for handler in self._lv3_handlers:
                handler.handle(req, res)

            # level 4: main handling
            lv4_handle(req, res)

            # level 5: response handling
            for handler in self._lv5_handlers:
                handler.handle(req, res)

            # level 6: send handling
            return self._lv6_handler.handle(req, res, wsgi_send)
        except Exception as e:
            # level 7: error handling
            handled = False
            for handler in self._lv7_handlers:
                if handler.handle(req, res, e):
                    handled = True
            if not handled:
                raise e

            # level 8: error log handling
            self._lv8_handler.handle(req, res, e)

            # level 9: send error response
            return self._lv9_handler.handle(req, res, wsgi_send)

    def _init_routes(self):
        for type, obj in self.injector.com_inst.items():
            if isinstance(obj, Controller):
                self._add_ctl(obj)

    def _add_ctl(self, ctl):
        base_path = getattr(ctl, COM_ATTR)['route_path']
        route = Route(base_path)

        for m in dir(ctl):
            mm = getattr(ctl, m)
            if COM_ATTR in dir(mm):
                mm_attrs = getattr(mm, COM_ATTR)
                if 'raw_route' not in mm_attrs:
                    continue
                raw_route = mm_attrs['raw_route']
                method = raw_route[0]
                path = raw_route[1]
                req_type = raw_route[2]
                route.add_spec(method, path, req_type, mm)

        self.router.add_route(route)
