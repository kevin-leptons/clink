'''
SYNOPSIS

    class MongoNode

DESCRIPTION

    Implement IMongoNode.
'''

from pymongo import MongoClient, IndexModel

from .error import DocumentNotExist, DocumentIndexError
from .imongo_node import IMongoNode


class MongoNode(IMongoNode):
    def __init__(self, url, db_name, doc_specs):
        self._url = url
        self._db_name = db_name
        self._doc_specs = doc_specs
        self._client = None

        self._doc_names = [s.name for s in doc_specs]
        self._create_docs()

    def instance(self):
        if self._client is None:
            self._client = MongoClient(host=self._url)
        return self._client[self._db_name]

    def doc(self, name):
        if name not in self._doc_names:
            raise DocumentNotExist
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

    def _create_docs(self):
        # ensure that database have documents with valid indexs
        db = self.instance()
        db_doc_names = db.collection_names()
        for spec in self._doc_specs:
            if spec.name not in db_doc_names:
                # document doesn't exist, create it and it's indexes
                doc = db[spec.name]
                doc.create_indexes(spec.indexes)
            else:
                # document is exist, verify it's indexes
                doc = db[spec.name]
                doc_index_info = doc.index_information()
                self._verify_indexes(spec, doc_index_info)

    def _verify_indexes(self, doc_spec, doc_index_info):
        # doc_sec: clink.db.MongoDocSpec
        # doc_index_info: result of pymongo.Collection.index_information()
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
