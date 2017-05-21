from clink.etc import URL_SLASH

from .error import RouteExistError, PathNotFoundError, HandleNotFoundError
from .type import MapNode, NodeAction


class Router():
    '''
    Store and find routes 
    '''

    def __init__(self, routes=[]):
        '''
        :param list<Router> routes:
        '''

        self._root_node = MapNode('/')
        self.add_routes(routes)

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

    def find_handle(self, method, content_type, path):
        '''
        Find handle which match with request

        :param str method:
        :param str content_type:
        :param str path:
        :rtype: function
        :raise PathNotFoundError:
        :raise HandleNotFoundError:
        '''

        node = self._find_node(path)
        if node is None or len(node.actions) == 0:
            raise PathNotFoundError(path)
        for action in node.actions:
            if action.method != method.lower():
                continue
            if action.content_type != content_type:
                continue
            return action.handle
        raise HandleNotFoundError(method, content_type, path)


    def _find_node(self, path):
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
