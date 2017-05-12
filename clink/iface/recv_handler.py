'''
SYNOPSIS

    interface IRecvHandler

DESCRIPTION

    Interface to initiallize request and response in WSGI application.
'''

from abc import ABC, abstractmethod


class IRecvHandler(ABC):
    @abstractmethod
    def handle(self, req, res, wsgi_env):
        pass
