from pymongo import MongoClient
from pytest import fixture

DB_URL = 'mongodb://localhost'
DB_NAME = 'clink'


@fixture(scope='module')
def clean_db():
    client = MongoClient(DB_URL)
    client.drop_database(DB_NAME)
    client.close()

    return {
        'dburl': DB_URL,
        'dbname': DB_NAME
    }
