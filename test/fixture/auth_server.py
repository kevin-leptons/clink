from os import environ
from pytest import fixture
from multiprocessing import Process
from time import sleep

from lib import auth_app
from lib.invoker import Invoker

ROOT_PWD = '123456'
ROOT_EMAIL = environ['CLINK_TEST_ROOT_EMAIL']
ROOT_EMAIL_PWD = environ['CLINK_TEST_ROOT_EMAIL_PWD']
ROOT_EMAIL_SERVER = environ['CLINK_TEST_ROOT_EMAIL_SERVER']
ROOT_EMAIL_SERVER_PORT = int(environ['CLINK_TEST_ROOT_EMAIL_SERVER_PORT'])


@fixture(scope='module')
def auth_server(request):
    port = 8080
    args = (ROOT_PWD, ROOT_EMAIL, ROOT_EMAIL_PWD,
            ROOT_EMAIL_SERVER, ROOT_EMAIL_SERVER, port)
    p = Process(target=auth_app.start, args=args)
    p.start()
    sleep(3)

    def free():
        p.terminate()
        p.join()

    request.addfinalizer(free)

    return Invoker('http://localhost:%i' % port, None,
                   'root', ROOT_PWD, ROOT_EMAIL)
