from jsonschema import validate, ValidationError
from clink.error.http import Http400Error, Http403Error, Http413Error


def header(schema):
    '''
    Verify header of HTTP message. It assume that HTTP header was converted
    into Python dictionary

    :param dict schema:
    '''

    def decorator_fn(target_fn):
        def new_fn(obj, req, res):
            try:
                validate(req.header, schema)
            except ValidationError as e:
                raise Http400Error(req, 'Invalid header: ' + str(e))
            target_fn(obj, req, res)
        return new_fn
    return decorator_fn


def body(schema):
    '''
    Verify body of HTTP message. It assume that HTTP body was converted
    into Python dictionary

    :param dict schema:
    '''

    def decorator_fn(target_fn):
        def new_fn(obj, req, res):
            try:
                validate(req.body, schema)
            except ValidationError as e:
                raise Http400Error(req, 'Invalid body: ' + str(e))
            target_fn(obj, req, res)
        return new_fn
    return decorator_fn


def allow_remote(*args):
    '''
    Allow remote addresses

    :param tuple args:
    '''

    def decorator_fn(target_fn):
        def handle(self, req, res):
            if req.remote_addr not in args:
                raise Http403Error(req)
            target_fn(self, req, res)
        return handle
    return decorator_fn


def denie_remote(*args):
    '''
    Denie remote addresses

    :param tuple args:
    '''

    def decorator_fn(target_fn):
        def handle(self, req, res):
            if req.remote_addr in args:
                raise Http403Error(req)
            target_fn(self, req, res)
        return handle
    return decorator_fn


def max_content_size(size):
    '''
    Allow max size of body

    :param int size:
    '''

    def decorator_fn(target_fn):
        def handle(self, req, res):
            if req.content_length > size:
                raise Http413Error(req)
            target_fn(self, req, res)
        return handle
    return decorator_fn
