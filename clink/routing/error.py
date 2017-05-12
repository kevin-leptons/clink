'''
SYNOPSIS

    class RouteExistError
    class RoutePathError

DESCRIPTION

    Error occurs during routing.
'''


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
