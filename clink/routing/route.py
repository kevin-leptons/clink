from .error import RouteHandleError


class Route():
    '''
    Specify a route in a map
    '''

    def __init__(self, path, method, req_type, handle):
        '''
        :param str path:
        :param str method:
        :param str req_type:
        :param function handle:
        '''

        if not callable(handle):
            raise RouteHandleError(handle)

        self.path = path
        self.method = method
        self.req_type = req_type
        self.handle = handle
