from clink.com import COM_ATTR
from clink.mime.type import MIME_JSON


def path(path):
    def new_fn(target_fn):
        target_fn._path = path
        if COM_ATTR in dir(target_fn):
            target_fn.__clink['route_path'] = path
        else:
            target_fn.__clink = {'route_path': path}
        return target_fn
    return new_fn


def map(method, path, req_type):
    def decorator_fn(target_fn):
        raw_route = (method, path, req_type)
        if COM_ATTR in dir(target_fn):
            target_fn.__clink['raw_route'] = raw_route
        else:
            target_fn.__clink = {'raw_route': raw_route}
        return target_fn
    return decorator_fn


def get(path):
    return map('get', path, None)


def post(path, req_type=MIME_JSON):
    return map('post', path, req_type)


def put(path, req_type=MIME_JSON):
    return map('put', path, req_type)


def patch(path, req_type=MIME_JSON):
    return map('patch', path, req_type)


def delete(path):
    return map('delete', path, None)
