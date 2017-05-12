'''
SYNOPSIS

    interface ISendHandler

DESCRIPTION

    Interface to send response message to client in WSGI application.
'''

from abc import ABC, abstractmethod


class ISendHandler(ABC):
    @abstractmethod
    def handle(self, req, res, wsgi_send):
        pass
