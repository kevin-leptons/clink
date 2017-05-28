from abc import ABC, abstractmethod
from clink.com.type import Component


class IPipeHandler(Component):
    pass


class ILv0Handler(IPipeHandler, ABC):
    '''
    Receive handling
    '''

    @abstractmethod
    def handle(self, req, res, env):
        '''
        :param Request req:
        :param Response res:
        :param dict env:
        '''

        pass


class ILv1Handler(IPipeHandler, ABC):
    '''
    Pre-Routing handling
    '''

    @abstractmethod
    def handle(self, req, res):
        '''
        :param Request req:
        :param Response res:
        '''

        pass


class ILv2Handler(IPipeHandler, ABC):
    '''
    Routing
    '''

    @abstractmethod
    def handle(self, req):
        '''
        :param Request req:
        :rtype: function
        '''

        pass


class ILv3Handler(IPipeHandler, ABC):
    '''
    Pre-Main handling
    '''

    @abstractmethod
    def handle(self, req, res):
        '''
        :param Request req:
        :param Response res:
        '''

        pass


class ILv4Handler(IPipeHandler):
    '''
    Main handling. It must be function, but we can't define interface
    for functions. Here are symbolic interface.
    '''

    pass


class ILv5Handler(IPipeHandler, ABC):
    '''
    Responding handling
    '''

    @abstractmethod
    def handle(self, req, res):
        '''
        :param Request req:
        :param Response res:
        '''

        pass


class ILv6Handler(IPipeHandler, ABC):
    '''
    Sending handling
    '''

    @abstractmethod
    def handle(self, req, res, wsgi_send):
        '''
        :param Request req:
        :param Response res:
        :param function wsgi_send:
        '''

        pass


class ILv7Handler(IPipeHandler, ABC):
    '''
    Error handling
    '''

    @abstractmethod
    def handle(self, req, res, e):
        '''
        :param Request req:
        :param Response res:
        :param Exception e:
        '''

        pass


class ILv8Handler(IPipeHandler, ABC):
    '''
    Error logging handling
    '''

    @abstractmethod
    def handle(self, req, res, e):
        '''
        :param Request req:
        :param Response res:
        :param Exception e:
        '''

        pass


class ILv9Handler(ILv6Handler):
    '''
    Sending error handling
    '''

    pass
