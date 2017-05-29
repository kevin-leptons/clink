from .error import RouteMethodError, RoutePathError, RouteHandleError

_ALLOWED_METHODS = ['get', 'post', 'put', 'patch', 'delete', 'option', 'head']


class Route():
    '''
    Specify a route in a map
    '''

    def __init__(self, method, content_type, path, handle):
        '''
        :param str method:
        :param str content_type:
        :param function handle:
        '''

        self._verify_method(method)
        self._verify_path(path)
        self._verify_handle(handle)

        self.method = method
        self.content_type = content_type
        self.path = path
        self.handle = handle

    def _verify_path(self, path):
        if len(path) == 0:
            return
        if path[0] == '/' or path[-1:] == '/':
            raise RoutePathError(path)

    def _verify_method(self, method):
        if method.lower() not in _ALLOWED_METHODS:
            raise RouteMethodError(method)

    def _verify_handle(self, handle):
        if not callable(handle):
            raise RouteHandleError(handle)
