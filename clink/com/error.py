class ComInvalidError(Exception):
    def __init__(self, com_type):
        self._msg = com_type.__name__

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
