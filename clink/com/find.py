import inspect
from collections import deque

from clink.com.type import Component


def find(module, com_type=Component):
    '''
    Find class which extends from com_type in module

    :param module module:
    :param class com_type:
    '''

    coms = []
    mod_que = deque([module])

    while len(mod_que) > 0:
        mod = mod_que.popleft()
        for name in dir(mod):
            a = getattr(mod, name)
            if inspect.ismodule(a):
                if a.__name__ != mod.__name__ + '.' + name:
                    continue
                mod_que.append(a)
            elif inspect.isclass(a):
                if a.__module__ != mod.__name__:
                    continue
                if not issubclass(a, com_type):
                    continue
                coms.append(a)
    return coms
