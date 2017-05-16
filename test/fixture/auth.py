from pytest import fixture

from clink.auth import Auth


@fixture(scope='session')
def auth(dbnode):
    return Auth(dbnode, 'root-pwd', 'root@email.com', 'jwt-key')
