'''
SYNOPSIS

    class MongoNode

DESCRIPTION

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

from pymongo import MongoClient, IndexModel

from clink.com import com, Component

from .error import DocumentNotExist, DocumentIndexError, DocSpecExit
from .type import MongoConf


@com(MongoConf)
class MongoService(Component):
    def __init__(self, conf):
        self._conf = conf
        self._doc_specs = []
        self._client = None
        self._doc_names = []

    def use_docspecs(self, doc_specs):
        for spec in doc_specs:
            self.use_docspec(spec)

    def use_docspec(self, doc_spec):
        db = self.instance()
        db_docs = db.collection_names()

        if doc_spec.name in db_docs:
            self._verify_spec(doc_spec)
        else:
            self._create_spec(doc_spec)

        self._doc_names.append(doc_spec.name)

    def _create_spec(self, doc_spec):
        db = self.instance()
        doc = db[doc_spec.name]

        if len(doc_spec.indexes) > 0:
            doc.create_indexes(doc_spec.indexes)

    def _verify_spec(self, doc_spec):
        # doc_sec: clink.db.MongoDocSpec
        # doc_index_info: result of pymongo.Collection.index_information()

        db = self.instance()
        doc_index_info = db[doc_spec.name].index_information()
        for index in doc_spec.indexes:
            # check index is exist
            if index.document['name'] not in doc_index_info:
                raise DocumentIndexError(doc_spec.name, index)

            # reconstruct index model from information
            index_name = index.document['name']
            doc_info = doc_index_info[index_name]
            doc_info_key = doc_info['key']
            doc_info['name'] = index_name
            del doc_info['key']
            doc_index = IndexModel(doc_info_key, **doc_info)

            # compare two index
            if not self._index_is_equal(index, doc_index):
                raise DocumentIndexError(doc_spec.name, index)

    def _index_is_equal(self, index_1, index_2):
        # index_1, index_2: pymongo.IndexModel
        doc_1 = index_1.document
        doc_2 = index_2.document
        for k in doc_1:
            if k not in doc_2:
                return False
            if doc_1[k] != doc_2[k]:
                return False
        return True

    def instance(self):
        self._connect()
        return self._client[self._conf.dbname]

    def doc(self, name):
        if name not in self._doc_names:
            raise DocumentNotExist(name)
        return self.instance()[name]

    def docs(self, *args):
        for name in args:
            if name not in self._doc_names:
                raise DocumentNotExist(name)
        db = self.instance()
        return tuple([db[name] for name in args])

    def close(self):
        if self._client is not None:
            self._client.close()

    def clear(self):
        self._connect()
        self._client.drop_database(self._conf.dbname)

    def _connect(self):
        if self._client is None:
            self._client = MongoClient(host=self._conf.dburl)
