from abc import ABC, abstractmethod
from clink.com.type import Component


class ILv0Handler(Component, ABC):
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


class ILv1Handler(Component, ABC):
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


class ILv2Handler(Component, ABC):
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


class ILv3Handler(Component, ABC):
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


class ILv4Handler(Component):
    '''
    Main handling. It must be function, but we can't define interface
    for functions. Here are symbolic interface.
    '''

    pass


class ILv5Handler(Component, ABC):
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


class ILv6Handler(Component, ABC):
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


class ILv7Handler(Component, ABC):
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


class ILv8Handler(Component, ABC):
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
