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

from .http_error import Http404Error, Http405Error, Http406Error

_URL_SLASH = '/'
_PARAM_CHAR = ':'


class RouteExistError(Exception):
    def __init__(self, spec):
        self.spec = spec
        self._msg = '%s %s; %s' % (
            spec.method, spec.path, spec.req_type
        )

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
        self.specs = []


class RouteSpec():
    def __init__(self, method, path, handler, req_type):
        self.method = method
        self.path = path
        self.handler = handler
        self.req_type = req_type


class Route():
    def __init__(self, base_path):
        if not self.verify_path(base_path):
            raise RoutePathError(base_path)
        self.base_path = base_path
        self.specs = []

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

    def map(self, method, path, req_type='application/json'):
        if not self.verify_path(path):
            raise RoutePathError(path)

        def decorator_fn(target_fn):
            abs_path = os.path.join(self.base_path, path)
            spec = RouteSpec(method, abs_path, target_fn, req_type)
            self.specs.append(spec)
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
            for spec in route.specs:
                self.add_route(spec)

    def find_route_handler(self, req):
        node = self.find_node(req.path)
        if node is None:
            raise Http404Error(req)
        for spec in node.specs:
            method_ok = spec.method == req.method.lower()
            type_ok = spec.req_type == req.content_type
            if (not method_ok) and (not type_ok):
                continue
            if (not method_ok) and type_ok:
                raise Http405Error(req)
            if (not type_ok) and method_ok:
                raise Http406Error(req)
            return spec.handler
        raise Http404Error(req)

    def add_route(self, spec):
        # search and add nodes
        node = self._root_route
        if spec.path != _URL_SLASH:
            node_names = spec.path.split(_URL_SLASH)
            node_names = list(filter(''.__ne__, node_names))
            for node_name in node_names:
                if node_name not in node.child:
                    node.child[node_name] = RouteNode(node_name)
                node = node.child[node_name]

        # add handle
        if self._spec_is_exist(node, spec):
            raise RouteExistError(spec)
        node.specs.append(spec)

    def find_node(self, path):
        node = self._root_route
        if path != _URL_SLASH:
            node_names = path.split(_URL_SLASH)
            node_names = list(filter(''.__ne__, node_names))
            for node_name in node_names:
                if node_name not in node.child:
                    return None
                node = node.child[node_name]
        return node

    def _spec_is_match(self, spec_1, spec_2):
        if spec_1.method != spec_2.method:
            return False
        if spec_1.req_type != spec_2.req_type:
            return False
        return True

    def _spec_is_exist(self, node, spec):
        for node_spec in node.specs:
            if self._spec_is_match(node_spec, spec):
                return True
        return False
