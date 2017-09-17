from clink.com import read_stamp
from clink.iface import ILv2Handler
from clink.error.http import Http400Error, Http404Error, Http405Error

from .error import RouteExistError
from .route import Route
from .mapper import CTL_PATH_ATTR, CTL_METHOD_ATTR


class Router(ILv2Handler):
    '''
    Store and find routes
    '''

    def __init__(self, routes=[]):
        '''
        :param list<Router> routes:
        '''

        self._map = {}
        self.add_routes(routes)

    def add_ctl(self, ctl):
        '''
        Collect routing information from controller

        :param object ctl:
        '''

        ctl_type = type(ctl)
        ctl_path = read_stamp(ctl, CTL_PATH_ATTR)
        for attr_name in dir(ctl_type):
            ctl_attr = getattr(ctl_type, attr_name)
            try:
                ctl_method = read_stamp(ctl_attr, CTL_METHOD_ATTR)
                abs_path = ctl_path + ctl_method.path
                abs_path = abs_path.replace('//', '/')
                if len(abs_path) > 1 and abs_path[-1] == '/':
                    abs_path = abs_path[:len(abs_path) - 1]
                route = Route(
                    abs_path, ctl_method.method, ctl_method.req_type,
                    getattr(ctl, attr_name)
                )
                self.add_route(route)
            except KeyError:
                pass
            except TypeError:
                pass

    def add_route(self, route):
        '''
        Put route into map

        :param Route route:
        :raise RouteExistError:
        '''
        if route.path not in self._map:
            self._map[route.path] = {}
        if route.method not in self._map:
            self._map[route.path][route.method] = {}
        if route.req_type in self._map[route.path][route.method]:
            raise RouteExistError(route)
        self._map[route.path][route.method][route.req_type] = route

    def add_routes(self, routes):
        '''
        Put routes into map

        :param list[Route] routes:
        '''

        for route in routes:
            self.add_route(route)

    def handle(self, req):
        '''
        Find handle which match with request

        :param Request req:
        :rtype: function
        :raise Http400Error:
        :raise Http404Error:
        :raise Http405Error:
        '''

        path = req.path
        method = req.method

        if path not in self._map:
            raise Http404Error(req)
        if method not in self._map[path]:
            raise Http405Error(req)
        if req.content_type not in self._map[path][method]:
            raise Http400Error(req)
        return self._map[path][method][req.content_type].handle
