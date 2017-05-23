from clink.com import stamp, Component


class MongoDocSpec():
    '''
    Specify an mongo document
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
        return self._name

    @property
    def indexes(self):
        return self._indexes


@stamp()
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
