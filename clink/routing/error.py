class CtlSpecError(Exception):
    def __init__(self, ctl):
        self._msg = '%s MUST contains COM_ATT.ROUTE_PATH_ATTR' % ctl.__name__

    def __str__(self):
        return self._msg


class PathNotFoundError(Exception):
    def __init__(self, path):
        self._msg = path

    def __str__(self):
        return self._msg


class HandleNotFoundError(Exception):
    def __init__(self, method, content_type, path):
        self._msg = '%s:%s:%s' % (method, content_type, path)

    def __str__(self):
        return self._msg


class RouteExistError(Exception):
    def __init__(self, route):
        self._msg = '%s %s %s' % (
            route.method, route.content_type, route.path
        )

    def __str__(self):
        return self._msg


class RouteMethodError(Exception):
    def __init__(self, method):
        self._msg = 'Method %s not allowed' % method

    def __str__(self):
        return self._msg


class RoutePathError(Exception):
    def __init__(self, path):
        self._msg = '%s must not contains slash at begin and end' % path

    def __str__(self):
        return self._msg


class RouteHandleError(Exception):
    def __init__(self, handle):
        self._msg = 'Handle %s must be callable' % handle

    def __str__(self):
        return self._msg
