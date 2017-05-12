"""
SYNOPSIS

    class Router

DESCRIPTION

    Implement IRouter.
"""

from ..error.http import Http404Error, Http405Error, Http406Error
from ..iface import IRouter
from ..etc import URL_SLASH
from .error import RouteExistError
from .type import RouteNode


class Router(IRouter):
    def __init__(self, routes):
        self._root_route = RouteNode('/')
        for route in routes:
            for spec in route.specs:
                self.add_route(spec)

    def find_handle(self, req):
        node = self.find_node(req.path)
        if node is None or len(node.specs) == 0:
            raise Http404Error(req)
        m_ok_specs = [s for s in node.specs if s.method == req.method.lower()]
        if len(m_ok_specs) == 0:
            raise Http405Error(req)
        for spec in m_ok_specs:
            if spec.req_type == req.content_type:
                return spec.handler
        raise Http406Error(req)

    def add_route(self, spec):
        # search and add nodes
        node = self._root_route
        if spec.path != URL_SLASH:
            node_names = spec.path.split(URL_SLASH)
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
        if path != URL_SLASH:
            node_names = path.split(URL_SLASH)
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
