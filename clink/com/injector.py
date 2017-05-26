from collections import deque

from .label import read_stamp, COM_DPDC_ATTR
from .type import Primitive, Component
from .error import CircleComError, ComExistError, ComDepedencyError, \
                   ComCreationError, InjectorLoadingError, PrimError


class Injector():
    '''
    Object management
    '''

    def __init__(self):
        self._com_dict = {}
        self._com_layer = []
        self.com_inst = {}
        self._loaded = False

    def add_prim(self, com_obj):
        '''
        Put an instance of component under management. Instance MUST be
        primitive

        :param clink.com.Component com_obj:
        :raise ComExistError:
        :raise ComDepedencyError:
        '''

        com_type = type(com_obj)
        if not issubclass(com_type, Primitive):
            raise TypeError(
                '%s is not subclass of %s' % (com_type, Primitive)
            )
        if com_type in self._com_dict:
            raise ComExistError(com_type)

        if len(read_stamp(com_type, COM_DPDC_ATTR)) > 0:
            raise ComDepedencyError(com_type, 'MUST NOT contains dependency')

        self._com_dict[com_type] = []
        self.com_inst[com_type] = com_obj

    def add_com(self, com_type):
        '''
        Put an component under management

        :param class com_type:
        :raise ComExistError:
        '''

        if com_type in self._com_dict:
            raise ComExistError(com_type)

        self._com_dict[com_type] = read_stamp(com_type, COM_DPDC_ATTR)

    def add_coms(self, com_types):
        '''
        Put components under management

        :param list[class] com_types:
        '''

        for com_type in com_types:
            self.add_com(com_type)

    def load(self):
        '''
        Start to create instances of all of components
        '''
        self._expand_com()
        self._mkcom_layer()
        self._mkcom_instance()
        self._loaded = True

    def ref(self, com_type):
        '''
        Return reference to component

        :param class com_type:
        :rtype: object
        '''

        self._must_loaded()
        if com_type not in self.com_inst:
            return None

        return self.com_inst[com_type]

    def sub_ref(self, com_type):
        '''
        Return references to components which extends from com_type

        :param class com_type:
        :rtype: list[object]
        '''

        self._must_loaded()

        coms = []
        for key in self.com_inst:
            if isinstance(self.com_inst[key], com_type):
                coms.append(self.com_inst[key])

        return coms

    def _must_loaded(self):
        if not self._loaded:
            raise InjectorLoadingError()

    def _expand_com(self):
        com_queue = deque(self._com_dict.keys())

        while len(com_queue) > 0:
            com_type = com_queue.popleft()
            req_coms = read_stamp(com_type, COM_DPDC_ATTR)

            if com_type not in self._com_dict:
                self._com_dict[com_type] = req_coms
            for req_com in req_coms:
                if not issubclass(req_com, Component):
                    raise TypeError(
                        '%s is not component in %s' % (req_com, com_type)
                    )
                if req_com not in self._com_dict:
                    com_queue.append(req_com)

    def _mkcom_layer(self):
        com_list = list(self._com_dict.keys())

        while len(com_list) > 0:
            layer = []
            for com_type in com_list:
                in_layer = True
                for req_com in self._com_dict[com_type]:
                    if req_com in com_list:
                        in_layer = False
                        break
                if in_layer is True:
                    layer.append(com_type)
                    com_list.remove(com_type)
            if len(layer) == 0:
                raise CircleComError(com_list)
            self._com_layer.append(layer)

    def _mkcom_instance(self):
        for layer in self._com_layer:
            for com_type in layer:
                if com_type in self.com_inst:
                    continue
                if issubclass(com_type, Primitive):
                    raise PrimError(com_type, 'has not instance')
                arg_types = tuple([t for t in self._com_dict[com_type]])
                args = tuple([self.com_inst[t] for t in arg_types])
                try:
                    self.com_inst[com_type] = com_type(*args)
                except TypeError as e:
                    raise ComCreationError(com_type, args)
