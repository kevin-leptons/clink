_STAMP_KEY = '__clink'
COM_DPDC_ATTR = 'dpdc'


def write_stamp(target, key, value):
    '''
    Write metadata into target

    :param object target:
    :param str key:
    :param object value:
    '''

    if _STAMP_KEY not in dir(target):
        setattr(target, _STAMP_KEY, {})
    stamp = getattr(target, _STAMP_KEY)
    stamp[key] = value


def read_stamp(target, key):
    '''
    Read metadata from target

    :param object target:
    :param str key:
    '''

    if _STAMP_KEY not in dir(target):
        raise TypeError('%s was not stamped' % target)
    stamp = getattr(target, _STAMP_KEY)
    if key not in stamp:
        raise KeyError('%s.%s' % (_STAMP_KEY, key))
    return stamp[key]


def stamp(*args):
    '''
    Mark an class become component with depedencies

    :param tuple args:
    '''

    def decorator_fn(target):
        write_stamp(target, COM_DPDC_ATTR, args)
        return target
    return decorator_fn
