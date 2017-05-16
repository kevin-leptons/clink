from pytest import fixture
from multiprocessing import Process
from time import sleep

from lib import simple_app
from lib.invoker import Invoker


@fixture(scope='module')
def simple_server(request):
    port = 8080
    p = Process(target=simple_app.start, args=(port,))
    p.start()
    sleep(1)

    def free():
        p.terminate()
        p.join()

    request.addfinalizer(free)

    return Invoker('http://localhost:%i' % port)
