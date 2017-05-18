'''
SYSNOPSIS

    class Injector
        com_inst

        add_isnt(com_inst) 
        add_com(com_type)
        load()

DESCRIPTION

    com_inst is dictionary of instance of component. Key is type of component,
    value is isinstance of it. It must use as read only attribute, don't
    modify it.

    add_isnt() put an instance of component into list of instance of 
    component. com_inst argument must be subclass of clink.com.type.Component
    and marked as a component by clink.com.marker.com. add_isnt() only
    use to add configuration for other component because it doesn't support
    depedency component. It work like that for clear.

    add_com() put specification of component with com_type. com_type is
    type, not an instance. It must be subclass of clink.com.type.Component.
    Depedency components are specify via clink.com.marker.com.

    load() perform creating component by solve depedency components and
    put instance of depedency components to constructor.
'''

from collections import deque

from .type import Component
from .error import ComInvalidError, CircleComError, ComExistError 

CLINK_COM_ATTR = '__clink'


class Injector():
    def __init__(self):
        self._com_dict = {}
        self._com_layer = []
        self.com_inst = {}

    def add_isnt(self, com_obj):
        com_type = type(com_obj)
        if not isinstance(com_obj, Component):
            raise ComInvalidError(com_type)
        if CLINK_COM_ATTR not in dir(com_type):
            raise ComInvalidError(com_type)
        if com_type in self._com_dict:
            raise ComExistError(com_type)
        clink_spec = getattr(com_type, CLINK_COM_ATTR)
        if len(clink_spec['req_coms']) > 0:
            raise InvalidDepedencyError(com_type)

        self._com_dict[com_type] = []
        self.com_inst[com_type] = com_obj

    def add_com(self, com_type):
        methods = dir(com_type)
        if CLINK_COM_ATTR not in methods:
            raise ComInvalidError(com_type)
        if com_type in self._com_dict:
            raise ComExistError(com_type)
        clink_spec = getattr(com_type, CLINK_COM_ATTR)
        self._com_dict[com_type] = clink_spec['req_coms']

    def load(self):
        self._expand_com()
        self._mkcom_layer()
        self._mkcom_instance()

    def instance(self, type):
        if type not in self.com_inst:
            return None
        return self.com_inst[type]    

    def instanceof(self, com_type):
        coms = []
        for t in self.com_inst:
            if isinstance(self.com_inst[t], com_type):
                coms.append(self.com_inst[t])
        return coms

    def _expand_com(self):
        com_queue = deque(self._com_dict.keys())
        while len(com_queue) > 0:
            ct = com_queue.popleft()
            methods = dir(ct)
            if CLINK_COM_ATTR not in methods:
                raise ComInvalidError(ct)
            req_coms = getattr(ct, CLINK_COM_ATTR)['req_coms']
            if ct not in self._com_dict:
                self._com_dict[ct] = req_coms
            for t in req_coms:
                if t not in self._com_dict:
                    com_queue.append(t)

    def _mkcom_layer(self):
        com_list = list(self._com_dict.keys())
        while len(com_list) > 0:
            layer = []
            for ct in com_list:
                in_layer = True
                for dt in self._com_dict[ct]:
                    if dt in com_list:
                        in_layer = False
                        break
                if in_layer is True:
                    layer.append(ct)
                    com_list.remove(ct)
            if len(layer) == 0:
                raise CircleComError(com_list)
            self._com_layer.append(layer)

    def _mkcom_instance(self):
        for layer in self._com_layer:
            for com_type in layer:
                if com_type in self.com_inst:
                    continue
                arg_types = tuple([t for t in self._com_dict[com_type]])
                args = tuple([self.com_inst[t] for t in arg_types])
                self.com_inst[com_type] = com_type(*args)
