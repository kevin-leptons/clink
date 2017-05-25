from clink.dflow import verify, FormatError


road_schema = {'type': 'string', 'pattern': '^[a-zA-Z0-9 ]{6,32}$'}


@verify(road_schema)
def run_car(road):
        print('Car is running on the %s' % road)


class Car():
    @verify(None, road_schema)
    def run(self, road):
        print('Car is running on the %s' % road)


try:
    car = Car()
    car.run('1st Hell Street')
    run_car('1st Hell Street @@@')
except FormatError as e:
    print('Error: ', e)
