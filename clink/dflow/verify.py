from functools import wraps
from inspect import getargspec
from jsonschema import ValidationError, validate

from .error import FormatError


def verify(*schemas):
    '''
    Decorator, verify formating of input arguments

    :param tuple[dict] schemas:
    :rtype: function
    '''

    def decorator(target):
        argspec = getargspec(target)

        @wraps(target)
        def new_fn(*args, **kargs):
            fargs = args
            oargs_len = len(argspec.args)
            args_len = len(args)

            if args_len < oargs_len:
                fargs = list(args)
                apd_len = oargs_len - args_len - 1
                apd_args = argspec.defaults[-apd_len:]
                fargs.extend(apd_args)
                fargs = tuple(fargs)
            if len(schemas) != len(fargs):
                raise IndexError(schemas, fargs)

            for arg_index, (schema, arg) in enumerate(zip(schemas, fargs)):
                if schema is None:
                    continue
                try:
                    validate(arg, schema)
                except ValidationError as e:
                    name = '.'.join(e.absolute_path)
                    if len(name) == 0:
                        name = argspec.args[arg_index]
                    raise FormatError(name, e.instance, e.schema)
            return target(*args, **kargs)
        return new_fn
    return decorator
