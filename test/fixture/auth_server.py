from pytest import fixture
from multiprocessing import Process
from time import sleep

from lib import auth_app
from lib.invoker import Invoker


@fixture(scope='module')
def auth_server(request, clean_db):
    dburl = clean_db['dburl']
    dbname = clean_db['dbname']
    port = 8080

    p = Process(target=auth_app.start, args=(dburl, dbname, port))
    p.start()
    sleep(1)

    def free():
        p.terminate()
        p.join()

    request.addfinalizer(free)

    return Invoker('http://localhost:%i' % port)
