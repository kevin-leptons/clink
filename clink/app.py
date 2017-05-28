from inspect import ismodule

from .com import find, Injector
from .iface import IWsgi, IPipeHandler, ILv0Handler, ILv1Handler, ILv3Handler
from .iface import ILv5Handler, ILv6Handler, ILv7Handler, ILv8Handler
from .type import Request, Response, Controller
from .routing import Router
from .handler import RecvHandler, SendHandler
from .handler import ReqJsonHandler, ReqUrlEncodeHandler, ReqLogHandler
from .handler import ResJsonHandler, ResCorsHandler
from .handler import ErrorHttpHandler, ErrorLogHandler, DflowErrorHandler
from .handler import RoutingErrorHandler


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
        :param clink.AppConf conf:
        '''

        self.router = Router()
        self.injector = Injector()
        self.injector.add_prim(conf)

        self.injector.add_com(RecvHandler)
        self.injector.add_com(ReqLogHandler)
        self.injector.add_com(ReqJsonHandler)
        self.injector.add_com(ReqUrlEncodeHandler)
        self.injector.add_com(ResJsonHandler)
        self.injector.add_com(ResCorsHandler)
        self.injector.add_com(SendHandler)
        self.injector.add_com(ErrorHttpHandler)
        self.injector.add_com(DflowErrorHandler)
        self.injector.add_com(ErrorLogHandler)
        self.injector.add_com(RoutingErrorHandler)

    def add_handler(self, handler_type):
        '''
        Add handler to application

        :param class handler_type:
        '''

        if not issubclass(handler_type, IPipeHandler):
            raise TypeError('%s is not handler' % handler_type)

        self.injector.add_com(handler_type)

    def add_prim(self, *args):
        for prim_ref in args:
            self.injector.add_prim(prim_ref)

    def add_ctl(self, ctl_type):
        '''
        Add controller to application

        :param class ctl:
        '''

        if not issubclass(ctl_type, Controller):
            raise TypeError('%s is not controller' % ctl_type)

        self.injector.add_com(ctl_type)

    def add_ctls(self, module):
        '''
        Search controllers in module and add them to application
        '''

        if not ismodule(module):
            raise TypeError('%s is not module' % module)

        ctl_types = find(module, Controller)
        self.injector.add_coms(ctl_types)

    def load(self):
        '''
        Creeate instance of all of components, put it to ready state
        '''

        self.injector.load()
        self._init_routes()

        self._lv0_handler = self.injector.sub_ref(ILv0Handler)[0]
        self._lv1_handler = self.injector.sub_ref(ILv1Handler)[0]
        self._lv3_handlers = self.injector.sub_ref(ILv3Handler)
        self._lv5_handlers = self.injector.sub_ref(ILv5Handler)
        self._lv6_handler = self.injector.sub_ref(ILv6Handler)[0]
        self._lv7_handlers = self.injector.sub_ref(ILv7Handler)
        self._lv8_handler = self.injector.sub_ref(ILv8Handler)[0]
        self._lv9_handler = self._lv6_handler

    def __call__(self, wsgi_env, wsgi_send):
        '''
        Implemention of WSGI. That mean you can call instance of App by
        WSGI server to make application is available on network.

        :param dict wsgi_env:
        :param function wsgi_send:
        '''

        # level 0: recv handling
        req = Request()
        res = Response()

        try:
            # level 0 continue: receiving handling
            self._lv0_handler.handle(req, res, wsgi_env)

            # level 1: pre-routing handling
            self._lv1_handler.handle(req, res)

            # level 2: routing, find main handler
            lv4_handle = self.router.handle(req)

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
        for com_type, com_ref in self.injector.com_inst.items():
            if isinstance(com_ref, Controller):
                self.router.add_ctl(com_ref)
