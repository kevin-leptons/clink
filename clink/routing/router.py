import os
from clink.etc import URL_SLASH
from clink.com import read_stamp
from clink.iface import ILv2Handler

from .error import RouteExistError, PathNotFoundError, HandleNotFoundError
from .type import MapNode, NodeAction
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

        self._root_node = MapNode('/')
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

        # search and add nodes
        node = self._root_node
        if route.path != URL_SLASH:
            node_names = route.path.split(URL_SLASH)
            node_names = list(filter(''.__ne__, node_names))
            for node_name in node_names:
                if node_name not in node.child:
                    node.child[node_name] = MapNode(node_name)
                node = node.child[node_name]

        # add action to node
        action = NodeAction(route.method, route.content_type, route.handle)
        if self._action_is_exist(node, action):
            raise RouteExistError(route)
        node.actions.append(action)

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

        node = self._find_node(req.path)
        if node is None or len(node.actions) == 0:
            raise PathNotFoundError(req.path)
        for action in node.actions:
            if action.method != req.method.lower():
                continue
            if action.content_type != req.content_type:
                continue
            return action.handle
        raise HandleNotFoundError(req.method, req.content_type, req.path)

    def _find_node(self, path):
        '''
        notes: algorithm can be improve here
        '''
        node = self._root_node
        if path != URL_SLASH:
            node_names = path.split(URL_SLASH)
            node_names = list(filter(''.__ne__, node_names))
            for node_name in node_names:
                if node_name not in node.child:
                    return None
                node = node.child[node_name]
        return node

    def _action_is_exist(self, node, action):
        for node_action in node.actions:
            if node_action.method != action.method:
                continue
            if node_action.content_type != action.method:
                continue
            return True
        return False
