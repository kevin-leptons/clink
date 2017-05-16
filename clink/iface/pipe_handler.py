'''
SYNOPSIS

    interface IPipeHandler

DESCRIPTION

    Inteface to process pipe processing.
'''

from abc import ABC, abstractmethod


class IPipeHandler(ABC):
    @abstractmethod
    def handle(self, req, res, ctx):
        pass
