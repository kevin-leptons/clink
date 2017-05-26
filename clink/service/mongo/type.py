from clink.com import stamp, Primitive


class MongoDocSpec():
    '''
    Specify an mongo document in database
    '''

    def __init__(self, name, indexes):
        '''
        :param str name:
        :param list[pymongo.IndexModel] indexes:
        '''

        self._name = name
        self._indexes = indexes

    @property
    def name(self):
        '''
        Name of document
        '''

        return self._name

    @property
    def indexes(self):
        '''
        List of indexes of document
        '''

        return self._indexes


@stamp()
class MongoConf(Primitive):
    '''
    Specify information of mongo server

    :param str dburl:
    :param str dbname:
    '''

    def __init__(self, dburl, dbname):
        self._dburl = dburl
        self._dbname = dbname

    @property
    def dburl(self):
        '''
        URL to server, it follows forms

            - mongodb://domain/path
            - mongodb://<username>:<password>@domain/path
        '''

        return self._dburl

    @property
    def dbname(self):
        '''
        Name of database will be use
        '''

        return self._dbname
