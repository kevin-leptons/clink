from clink.com.type import Component
from clink.iface import IPipeHandler


class Lv0Handler(Component):
    pass


class Lv1Handler(Component):
    pass

class Lv2Handler(Component):
    pass


class Lv3Handler(Component, IPipeHandler):
    pass


class Lv4Handler(Component):
    pass


class Lv5Handler(Component, IPipeHandler):
    pass


class Lv6Handler(Component):
    pass


class Lv7Handler(Component):
    pass


class Lv8Handler(Component):
    pass


class Lv9Handler(Component):
    pass


class Controller(Lv4Handler):
    pass


class Service(Component):
    pass
