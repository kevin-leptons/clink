from jsonschema import validate, ValidationError
from clink.error.http import Http400Error


def header(schema):
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
    def decorator_fn(target_fn):
        def new_fn(obj, req, res):
            try:
                validate(req.body, schema)
            except ValidationError as e:
                raise Http400Error(req, 'Invalid body: ' + str(e))
            target_fn(obj, req, res)
        return new_fn
    return decorator_fn
