from clink.iface import IWsgi, ILv0Handler, ILv1Handler, ILv3Handler, \
                        ILv5Handler, ILv6Handler, ILv7Handler, ILv8Handler
from .type import Request, Response, Controller
from .routing import Router
from .handler import RecvHandler, SendHandler
from .handler import ReqJsonHandler, ReqUrlEncodeHandler, ReqLogHandler
from .handler import ResJsonHandler, ResCorsHandler
from .handler import ErrorHttpHandler, ErrorLogHandler, DflowErrorHandler
from clink.com.injector import Injector


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
        self.injector.add_ref(conf)

        self.add_com(RecvHandler)
        self.add_com(ReqLogHandler)
        self.add_com(ReqJsonHandler)
        self.add_com(ReqUrlEncodeHandler)
        self.add_com(ResJsonHandler)
        self.add_com(ResCorsHandler)
        self.add_com(SendHandler)
        self.add_com(ErrorHttpHandler)
        self.add_com(DflowErrorHandler)
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
