'''
SYNOPSIS

    interface IErrorHandler

DESCRIPTION

    Interface to handle error in pipe line processing.
'''

from abc import ABC, abstractmethod


class IErrorHandler(ABC):
    @abstractmethod
    def handle(self, req, res, e):
        pass
