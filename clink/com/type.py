from abc import ABC

COM_ATTR = '__clink'
COM_DEP = 'req_coms'


class Component(ABC):
    '''
    It doesn't contains anythings. It's use to mark an class become component
    '''

    pass


class Primitive(Component):
    '''
    Primitive components, it isn't create directly by injector. It must be
    add to injector by add_prim(). If other components depend on it, injector
    look up for it's instance, if not founds instance, raise error instead
    of create new one
    '''

    pass
