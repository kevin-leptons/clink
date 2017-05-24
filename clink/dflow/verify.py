import inspect
from jsonschema import ValidationError, validate
from .error import FormatError


def verify(*schemas):
    def decorator(target):
        arg_names = inspect.getargspec(target)[0]

        def new_fn(*args):
            if len(schemas) != len(args):
                raise IndexError('Schemas and arguments is invalid')
            for arg_index, (schema, arg) in enumerate(zip(schemas, args)):
                try:
                    validate(arg, schema)
                except ValidationError as e:
                    attr_name = '.'.join(e.absolute_path)
                    if len(attr_name) == 0:
                        attr_name = arg_names[arg_index]
                    raise FormatError(attr_name, e.instance, e.schema)
            target(*args)
        return new_fn
    return decorator
