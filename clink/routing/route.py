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

    def get(self, path):
        return self.map('get', path, None)

    def post(self, path, req_type=MIME_JSON):
        return self.map('post', path, req_type)

    def put(self, path, req_type=MIME_JSON):
        return self.map('put', path, req_type)

    def patch(self, path, req_type=MIME_JSON):
        return self.map('patch', path, req_type)

    def delete(self, path):
        return self.map('delete', path, None)

    def option(self, path):
        return self.map('option', path, None)

    def map(self, method, path, req_type):
        if not self.verify_path(path):
            raise RoutePathError(path)

        def decorator_fn(target_fn):
            abs_path = os.path.join(self.base_path, path)
            spec = RouteSpec(method, abs_path, target_fn, req_type)
            self.specs.append(spec)
        return decorator_fn

    def verify_path(self, path):
        if len(path) > 0:
            if path[0] == URL_SLASH:
                return False
        return True
