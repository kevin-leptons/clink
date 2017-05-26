from .type import Component, COM_ATTR, COM_DEP


class PrimError(Exception):
    def __init__(self, prim_type, msg):
        self.prim_type = prim_type
        self._msg = '%s %s' % (prim_type, msg)

    def __str__(self):
        return self._msg


class ComDepedencyError(Exception):
    def __init__(self, com_type, msg):
        self._msg = '%s: %s' % (com_type.__name__, msg)

    def __str__(self):
        return self._msg


class InjectorLoadingError(Exception):
    pass


class ComTypeError(Exception):
    def __init__(self, com_type):
        self._msg = '%s must extend from %s' % (type(Component))

    def __str__(self):
        return self._msg


class ComAttrError(Exception):
    def __init__(self, com_type):
        self._msg = '%s must contains %s.%s' (COM_ATTR, COM_DEP)

    def __str__(self):
        return self._msg


class CircleComError(Exception):
    def __init__(self, com_types):
        self._msg = ', '.join([t.__name__ for t in com_types])

    def __str__(self):
        return self._msg


class ComExistError(Exception):
    def __init__(self, com_type):
        self._msg = com_type.__name__

    def __str__(self):
        return self._msg


class ComCreationError(Exception):
    def __init__(self, com_type, args):
        self._msg = 'type=%s, args=%s' % (com_type, args)

    def __str__(self):
        return self._msg
