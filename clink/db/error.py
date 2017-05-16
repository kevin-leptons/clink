class DocSpecExit(Exception):
    def __init__(self, name):
        self._msg = name

    def __str__(self):
        return self._msg


class DocumentNotExist(Exception):
    def __init__(self, doc_name):
        self._doc_name = doc_name

    def __str__(self):
        return self._doc_name


class DocumentIndexError(Exception):
    def __init__(self, doc_name, req_index):
        index_doc = req_index.document
        attr_unique = None
        if 'unique' in index_doc:
            attr_unique = index_doc['unique']
        attr_min = None
        if 'min' in index_doc:
            attr_min = index_doc['min']
        attr_max = None
        if 'max' in index_doc:
            attr_max = index_doc['max']
        index_str = 'name={}; unique={}; min={}; max={}; key={};'.format(
            index_doc['name'], attr_unique, attr_min, attr_max,
            index_doc['key']
        )
        self._msg = 'document \'{}\' must be specify indexes: {}'.format(
            doc_name, index_str
        )

    def __str__(self):
        return self._msg
