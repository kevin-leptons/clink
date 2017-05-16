'''
SYNOPSIS

    interface IMongoNode

DESCRIPTION

    Interface for MongoDB node.

    __init__() method must save information about MongoDB server.

    instance() method must return connection.
    If connection wasn't established, create new connection.
    If connection was lost, reconnect and save new connection on success.

    doc() method must return document which specify by name.

    docs() method must return tuple of specify documents by names. if name
    of documents isn't in document specifies, raise error.

    close() method must close connection, release all of usage resources.

REFERENCES

    MongoDB - Wikipedia
        https://en.wikipedia.org/wiki/MongoDB
    PyMongo - APIs documents
        https://api.mongodb.com/python/current/index.html
'''

from abc import ABC, abstractmethod


class IMongoNode(ABC):
    _client = None

    @abstractmethod
    def __init__(self, host, db_name, doc_specs=[]):
        pass

    @abstractmethod
    def use_docspecs(self, doc_specs):
        pass

    @abstractmethod
    def instance(self):
        pass

    @abstractmethod
    def doc(self, name):
        pass

    @abstractmethod
    def docs(self, *args):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def clear(self):
        pass
