'''
SYNOPSIS

    interface IWsgi

DESCRIPTION

    HTTP Server with WSGI interface. Entry is method __call__().

REFERENCES

    WSGI - Wikipedia
        https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface

    PEP333 - Python Web Server Gateway Interface
        https://www.python.org/dev/peps/pep-0333/
'''

from abc import ABC, abstractmethod


class IWsgi(ABC):
    @abstractmethod
    def __call__(self, wsgi_env, wsgi_send):
        pass
