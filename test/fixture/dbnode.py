from pytest import fixture
from clink.db import MongoNode

DB_URL = 'mongodb://dev:dev@ds011158.mlab.com:11158/clink'
DB_NAME = 'clink'


@fixture(scope='session')
def dbnode(request):
    dbnode = MongoNode(DB_URL, DB_NAME)
    dbnode.clear()

    def free():
        dbnode.close()

    request.addfinalizer(free)
    return dbnode
