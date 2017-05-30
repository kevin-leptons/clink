from pytest import fixture
from multiprocessing import Process
from time import sleep

from lib import auth_app
from lib.invoker import Invoker


@fixture(scope='module')
def auth_server(request):
    port = 8080
    p = Process(target=auth_app.start, args=(port,))
    p.start()
    sleep(3)

    def free():
        p.terminate()
        p.join()

    request.addfinalizer(free)

    return Invoker('http://localhost:%i' % port)
