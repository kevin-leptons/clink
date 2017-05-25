from jsonschema import ValidationError, validate
from .error import FormatError


def verify(*schemas):
    '''
    Decorator, verify formating of input arguments

    :param tuple[dict] schemas:
    :rtype: function
    '''

    def decorator(target):
        def new_fn(*args, **kargs):
            if len(schemas) != len(args):
                raise IndexError('Schemas and arguments is invalid')
            for arg_index, (schema, arg) in enumerate(zip(schemas, args)):
                if schema is None:
                    continue
                try:
                    validate(arg, schema)
                except ValidationError as e:
                    raise FormatError(
                        '.'.join(e.absolute_path), e.instance, e.schema
                    )
            return target(*args, **kargs)
        return new_fn
    return decorator
