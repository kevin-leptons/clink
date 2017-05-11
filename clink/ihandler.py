'''
SYNOPSIS

    interface IHandler
    interface IErrorHandler

DESCRIPTION

    Describe interface allow process pipeline.
'''

from abc import ABC, abstractmethod


class IHandler(ABC):
    @abstractmethod
    def handle(self, req, res):
        pass


class IErrorHandler(ABC):
    @abstractmethod
    def handle(self, req, res, e):
        pass


class IRecvHandler(ABC):
    @abstractmethod
    def handle(self, req, res, wsgi_env):
        pass


class ISendHandler(ABC):
    @abstractmethod
    def handle(self, req, res, wsgi_send):
        pass
