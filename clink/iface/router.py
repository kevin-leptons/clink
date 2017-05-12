'''
SYNOPSIS

    interface IRouter

DESCRIPTION

    Interface to find handler from request.

    Detect request handle and url parameters. It's not support parameters in
    url for performace, let use arugments.
'''

from abc import ABC, abstractmethod


class IRouter(ABC):
    @abstractmethod
    def find_handle(self, req):
        pass
