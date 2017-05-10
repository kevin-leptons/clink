"""
SYNOPSIS

    class RouteExistError
    class RoutePathError

    class Route
    class RouteNode
    class Router

DESCRIPTION

    Detect request handle and url parameters. It's not support parameters in
    url for performace, let use arugments.
"""

import os

from .http_error import Http404Error

_URL_SLASH = '/'
_PARAM_CHAR = ':'


class RouteExistError(Exception):
    def __init__(self, method, path):
        self.method = method
        self.path = path
        self._msg = '%s %s' % (method, path)

    def __str___(self):
        return self._msg


class RoutePathError(Exception):
    def __init__(self, path):
        self.path = path

    def __str___(self):
        return self.path


class RouteNode():
    def __init__(self, name):
        self.name = name
        self.child = {}
        self.methods = {}


class Route():
    def __init__(self, base_path):
        if not self.verify_path(base_path):
            raise RoutePathError(base_path)
        self.base_path = base_path
        self.paths = []

    def get(self, path):
        return self.map('get', path)

    def post(self, path):
        return self.map('post', path)

    def put(self, path):
        return self.map('put', path)

    def patch(self, path):
        return self.map('patch', path)

    def delete(self, path):
        return self.map('delete', path)

    def option(self, path):
        return self.map('option', path)

    def map(self, method, path):
        if not self.verify_path(path):
            raise RoutePathError(path)

        def decorator_fn(target_fn):
            abs_path = os.path.join(self.base_path, path)
            self.paths.append((method, abs_path, target_fn))

        return decorator_fn

    def verify_path(self, path):
        if len(path) > 0:
            if path[0] == _URL_SLASH:
                return False
        return True


class Router:
    def __init__(self, routes):
        self._root_route = RouteNode('/')
        for route in routes:
            for path in route.paths:
                self.add_route(path[0], path[1], path[2])

    def find_route_handler(self, req):
        node = self.find_node(req.path, req.params)
        if node is None:
            raise Http404Error(req)
        if req.method.lower() not in node.methods:
            raise Http404Error(req)
        return node.methods[req.method.lower()]

    def add_route(self, method, path, handle):
        # search and add nodes
        node = self._root_route
        if path != _URL_SLASH:
            node_names = path.split(_URL_SLASH)
            node_names = list(filter(''.__ne__, node_names))
            for node_name in node_names:
                if node_name not in node.child:
                    node.child[node_name] = RouteNode(node_name)
                node = node.child[node_name]

        # add handle
        if method in node.methods:
            raise RouteExistError(method, path)
        node.methods[method] = handle

    def find_node(self, path, params):
        node = self._root_route
        if path != _URL_SLASH:
            node_names = path.split(_URL_SLASH)
            node_names = list(filter(''.__ne__, node_names))
            for node_name in node_names:
                if node_name not in node.child:
                    return None
                node = node.child[node_name]
        return node
