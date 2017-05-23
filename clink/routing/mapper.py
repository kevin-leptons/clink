from clink.mime.type import MIME_JSON
from clink.com.label import write_stamp
from .type import CtlMethod

CTL_PATH_ATTR = 'ctl_path'
CTL_METHOD_ATTR = 'ctl_method'


def path(path):
    '''
    Specify a path to controller

    :param str path:
    '''

    def decorator_fn(target):
        write_stamp(target, CTL_PATH_ATTR, path)
        return target
    return decorator_fn


def map(method, path, content_type):
    '''
    Specify a controller's method

    :param str method:
    :param str path:
    :param str content_type:
    '''

    def decorator_fn(target):
        ctl_method = CtlMethod(method, path, content_type)
        write_stamp(target, CTL_METHOD_ATTR, ctl_method)
        return target
    return decorator_fn


def get(path):
    '''
    Specify a GET controller's method

    :param str path:
    '''

    return map('get', path, None)


def post(path, content_type=MIME_JSON):
    '''
    Map a POST controller's method

    :param str path:
    :param str content_type:
    '''

    return map('post', path, content_type)


def put(path, content_type=MIME_JSON):
    '''
    Map a PUT controller's method

    :param str path:
    :param str content_type:
    '''

    return map('put', path, content_type)


def patch(path, content_type=MIME_JSON):
    '''
    Map a PATCH controller's method

    :param str path:
    :param str content_type:
    '''

    return map('patch', path, content_type)


def delete(path):
    '''
    Map a DELETE controller's method

    :param str path:
    :param str content_type:
    '''

    return map('delete', path, None)
