class ExistError(Exception):
    '''
    Specify for indexes is early exist
    '''

    def __init__(self, indexes):
        '''
        :param dict indexes:
        '''

        self.indexes = indexes


class NonExistError(Exception):
    '''
    Specify for indexes doesn't exist
    '''

    def __init__(self, indexes):
        '''
        :param dict indexes:
        '''

        self.indexes = indexes


class FormatError(Exception):
    '''
    Specify for data formating is invalid
    '''

    def __init__(self, name, value, schema):
        '''
        :param str name:
        :param object value:
        :param object req:
        '''

        self.name = name
        self.value = value
        self.schema = schema

        self._msg = 'name=%s, value=%s, schema=%s' % (name, value, schema)

    def __str__(self):
        return self._msg


class ExpiredError(Exception):
    '''
    Specify expirision error
    '''

    def __init__(self, indexes):
        '''
        :param dict indexes:
        '''

        self.indexes = indexes
