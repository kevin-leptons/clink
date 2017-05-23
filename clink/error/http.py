HTTP_STATUS_NAMES = {
    100: 'Continue',
    101: 'Switching Protocol',
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    203: 'Non-Authoritative Information',
    204: 'No Content',
    205: 'Reset Content',
    206: 'Partial Content',
    300: 'Multiple Choices',
    301: 'Moved Permanently',
    302: 'Not Found',
    303: 'See Other',
    304: 'Not Modified',
    305: 'Use Proxy',
    307: 'Temporary Redirect',
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Accepted',
    407: 'Proxy Authentication Required',
    408: 'Request Timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length Required',
    412: 'Precondition Failed',
    413: 'Request Entity Too Large',
    414: 'Request-URI Too Long',
    415: 'Unsupported Media Type',
    416: 'Requested Range Not Satisfiable',
    417: 'Expectation Failed',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
    505: 'HTTP Version Not Supported'
}


def code_to_str(code):
    '''
    Convert HTTP error code to string

    :param int code:
    :raise: HttpStatusError:
    '''

    if code not in HTTP_STATUS_NAMES:
        raise HttpStatusError(code)
    return '%i %s' % (code, HTTP_STATUS_NAMES[code])


class HttpStatusError(Exception):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return self.code


# only use this error with status in 4xx, 5xx
class HttpError(Exception):
    def __init__(self, status, req, msg=None):
        self.status = status
        self.req = req
        self._msg = 'status=%i, %s %s' % (status, req.method, req.path)
        self.msg = msg

    def __str__(self):
        return self._msg


class Http400Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(400, req, msg)


class Http401Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(401, req, msg)


class Http402Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(402, req, msg)


class Http403Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(403, req, msg)


class Http404Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(404, req, msg)


class Http405Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(405, req, msg)


class Http406Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(406, req, msg)


class Http407Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(407, req, msg)


class Http408Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(408, req, msg)


class Http409Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(409, req, msg)


class Http410Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(410, req, msg)


class Http411Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(411, req, msg)


class Http412Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(412, req, msg)


class Http413Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(413, req, msg)


class Http414Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(414, req, msg)


class Http415Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(415, req, msg)


class Http416Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(416, req, msg)


class Http417Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(417, req, msg)


class Http500Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(500, req, msg)


class Http501Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(501, req, msg)


class Http502Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(502, req, msg)


class Http503Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(503, req, msg)


class Http504Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(504, req, msg)


class Http505Error(HttpError):
    def __init__(self, req, msg=None):
        super().__init__(505, req, msg)


class HttpArgumentError(Exception):
    def __init__(self, arg_str):
        self.arg_str = arg_str

    def __str__(self):
        return self.arg_str
