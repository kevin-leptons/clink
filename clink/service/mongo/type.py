'''
SYNOPSIS

    class MongoDocSpec

DESCRIPTION

    Specify documents of MongoDB.

    indexes is list of pymongo.IndexModel.

REFERENCES

    pymongo.IndexModel
        https://api.mongodb.com/python/current/api/pymongo/operations.html#\
        pymongo.operations.IndexModel
    PyMongo - Create document index
        https://api.mongodb.com/python/current/api/pymongo/collection.html#\
        pymongo.collection.Collection.create_indexes
'''

from clink.com import com, Component


class MongoDocSpec():
    def __init__(self, name, indexes):
        self._name = name
        self._indexes = indexes

    @property
    def name(self):
        return self._name

    @property
    def indexes(self):
        return self._indexes


@com()
class MongoConf(Component):
    def __init__(self, dburl, dbname):
        self._dburl = dburl
        self._dbname = dbname

    @property
    def dburl(self):
        return self._dburl

    @property
    def dbname(self):
        return self._dbname
