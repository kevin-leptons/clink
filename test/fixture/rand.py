from pytest import fixture

from lib.rand import Rand


@fixture(scope='module')
def rand():
    return Rand()
