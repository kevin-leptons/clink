from os import environ
from pytest import fixture
from multiprocessing import Process
from time import sleep

from lib import auth_app
from lib.invoker import Invoker

ROOT_EMAIL = environ['CLINK_TEST_ROOT_EMAIL']
ROOT_EMAIL_PWD = environ['CLINK_TEST_ROOT_EMAIL_PWD']
ROOT_EMAIL_SERVER = environ['CLINK_TEST_ROOT_EMAIL_SERVER']


@fixture(scope='module')
def auth_server(request):
    port = 8080
    args = (ROOT_EMAIL, ROOT_EMAIL_PWD, ROOT_EMAIL_SERVER, port)
    p = Process(target=auth_app.start, args=args)
    p.start()
    sleep(4)

    def free():
        p.terminate()
        p.join()

    request.addfinalizer(free)

    return Invoker('http://localhost:%i' % port)
