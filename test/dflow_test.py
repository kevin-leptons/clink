from pytest import raises
from clink.dflow import verify, FormatError

road_schema = {'type': 'string', 'pattern': '^[a-z ]{6,32}$'}
road = '1st Hell Street'


class Car():
    @verify(None, road_schema)
    def run(self, road):
        print('Car is running on the %s' % road)


@verify(road_schema)
def run_car(road):
    print('Car is running on the %s' % road)


def test_verify_method():
    car = Car()
    with raises(FormatError):
        car.run(road)


def test_verify_fn():
    with raises(FormatError):
        run_car(road)
