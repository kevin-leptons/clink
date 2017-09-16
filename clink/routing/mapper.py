import re
from clink.type import HTTP_GET, HTTP_POST, HTTP_PUT, HTTP_DELETE, HTTP_PATCH
from clink.mime import MIME_JSON
from clink.com.label import write_stamp
from .error import RoutePathError
from .type import CtlMethod

CTL_PATH_ATTR = 'ctl_path'
CTL_METHOD_ATTR = 'ctl_method'

_ROUTE_PATH_REGEX = re.compile('^(/[^/]*|/[^/]+(/[^/]+)+)$')


def path(path):
    '''
    Specify a path to controller

    :param str path:
    '''

    if _ROUTE_PATH_REGEX.match(path) is None:
        raise RoutePathError(path, _ROUTE_PATH_REGEX)

    def decorator_fn(target):
        write_stamp(target, CTL_PATH_ATTR, path)
        return target
    return decorator_fn


def map(path, method, req_type):
    '''
    Specify a controller's method

    :param str path:
    :param str method:
    :param str req_type:
    '''

    if _ROUTE_PATH_REGEX.match(path) is None:
        raise RoutePathError(path, _ROUTE_PATH_REGEX)

    def decorator_fn(target):
        ctl_method = CtlMethod(path, method, req_type)
        write_stamp(target, CTL_METHOD_ATTR, ctl_method)
        return target
    return decorator_fn


def get(path):
    '''
    Specify a GET controller's method

    :param str path:
    '''

    return map(path, HTTP_GET, None)


def post(path, req_type=MIME_JSON):
    '''
    Map a POST controller's method

    :param str path:
    :param str req_type:
    '''

    return map(path, HTTP_POST, req_type)


def put(path, req_type=MIME_JSON):
    '''
    Map a PUT controller's method

    :param str path:
    :param str req_type:
    '''

    return map(path, HTTP_PUT, req_type)


def patch(path, req_type=MIME_JSON):
    '''
    Map a PATCH controller's method

    :param str path:
    :param str req_type:
    '''

    return map(path, HTTP_PATCH, req_type)


def delete(path, req_type=MIME_JSON):
    '''
    Map a DELETE controller's method

    :param str path:
    '''

    return map(path, HTTP_DELETE, req_type)
