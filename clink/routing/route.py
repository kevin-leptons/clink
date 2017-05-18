'''
SYNOPSIS

    class Route

DESCRIPTION

    Decorate function to add it's function to routing.
'''

import os

from ..mime.type import MIME_JSON
from ..etc import URL_SLASH
from .error import RoutePathError
from .type import RouteSpec


class Route():
    def __init__(self, base_path):
        if not self.verify_path(base_path):
            raise RoutePathError(base_path)
        self.base_path = base_path
        self.specs = []

    def add_spec(self, method, path, req_type, handler):
        if not self.verify_path(path):
            raise RoutePathError(path)

        abs_path = os.path.join(self.base_path, path) 
        spec = RouteSpec(method, abs_path, handler, req_type)
        self.specs.append(spec)


    def verify_path(self, path):
        if len(path) > 0:
            if path[0] == URL_SLASH:
                return False
        return True
