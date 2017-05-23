from pymongo import MongoClient, IndexModel
from clink.com import stamp, Component

from .error import DocumentNotExist, DocumentIndexError
from .type import MongoConf


@stamp(MongoConf)
class MongoSv(Component):
    '''
    MongoDB interface in application layer
    '''

    def __init__(self, conf):
        '''
        :param MongoConf conf:
        '''

        self._conf = conf
        self._doc_specs = []
        self._client = None
        self._doc_names = []

    def use_docspec(self, doc_spec):
        '''
        Put a document's specification under management

        :param MongoDocSpec doc_spec:
        '''

        db = self._instance()
        db_docs = db.collection_names()

        if doc_spec.name in db_docs:
            self._verify_spec(doc_spec)
        else:
            self._create_spec(doc_spec)

        self._doc_names.append(doc_spec.name)

    def use_docspecs(self, doc_specs):
        '''
        Put document's specifications under management

        :param list[MongoDocSpec] doc_specs:
        '''

        for spec in doc_specs:
            self.use_docspec(spec)

    def doc(self, name):
        '''
        Return document object

        :param str name:
        :rtype: pymongo.collection.Collection
        :raise DocumentNotExist:
        '''

        if name not in self._doc_names:
            raise DocumentNotExist(name)
        return self._instance()[name]

    def docs(self, *args):
        '''
        Return document objects

        :param tuple[str] args:
        :rtype: tuple[pymongo.collection.Collection]
        :raise DocumentNotExist:
        '''
        for name in args:
            if name not in self._doc_names:
                raise DocumentNotExist(name)
        db = self._instance()
        return tuple([db[name] for name in args])

    def close(self):
        '''
        Close connection to server
        '''

        if self._client is not None:
            self._client.close()

    def clear(self):
        '''
        Clear all of data in database
        '''

        self._connect()
        self._client.drop_database(self._conf.dbname)

    def _create_spec(self, doc_spec):
        db = self._instance()
        doc = db[doc_spec.name]

        if len(doc_spec.indexes) > 0:
            doc.create_indexes(doc_spec.indexes)

    def _verify_spec(self, doc_spec):
        '''
        Verify that document's specification is valid in database

        :param MongoDocSpec:
        :raise DocumentIndexError:
        '''

        db = self._instance()
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
        '''
        Compare between two indexes

        :param pymongo.IndexModel index_1:
        :param pymongo.IndexModel index_2:
        :rtype: bool
        '''

        # index_1, index_2: pymongo.IndexModel
        doc_1 = index_1.document
        doc_2 = index_2.document
        for k in doc_1:
            if k not in doc_2:
                return False
            if doc_1[k] != doc_2[k]:
                return False
        return True

    def _connect(self):
        '''
        Make sure that client connect to server
        '''

        if self._client is None:
            self._client = MongoClient(host=self._conf.dburl)

    def _instance(self):
        '''
        Return instance of database object

        :rtype: pymongo.database.Database
        '''

        self._connect()
        return self._client[self._conf.dbname]
