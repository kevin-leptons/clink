import os
from clink.com import read_stamp
from clink.iface import ILv2Handler
from clink.error.http import Http404Error, Http405Error, Http406Error
from clink.mime import MIME_JSON

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
                abs_path = ctl_path
                if len(ctl_method.path) > 0:
                    abs_path = os.path.join(ctl_path, ctl_method.path)
                if ctl_method.method in ['post', 'put', 'patch']:
                    if ctl_method.content_type is None:
                        ctl_method.content_type = MIME_JSON
                route = Route(
                    ctl_method.method, ctl_method.content_type,
                    abs_path, getattr(ctl, attr_name)
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
        if route.content_type in self._map[route.path][route.method]:
            raise RouteExistError(route)
        self._map[route.path][route.method][route.content_type] = route

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
        :raise PathNotFoundError:
        :raise HandleNotFoundError:
        '''

        path = self._clear_path(req.path)
        method = req.method
        content_type = req.content_type

        if path not in self._map:
            raise Http404Error(req)
        if method not in self._map[path]:
            raise Http405Error(req)
        if content_type not in self._map[path][method]:
            raise Http406Error(req)
        return self._map[path][method][content_type].handle

    def _clear_path(self, path):
        if len(path) > 1 and path[0] == '/':
            path = path[1:]
        if len(path) > 1 and path[-1] == '/':
            path = path[:len(path) - 1]
        return path
