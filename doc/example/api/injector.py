from clink.com import Injector, Component, com


@com()
class Engine(Component):
    def __init__(self, name):
        self.name = name


@com(Engine)
class Car(Component):
    def __init__(self, engine):
        self.engine = engine

    def info(self):
        return 'A car with %s engine' % self.engine.name


@com(Car)
class Human(Component):
    def __init__(self, car):
        self.car = car

    def drive(self):
        print('I drive %s' % self.car.info())


engine = Engine('Turbo v8')
injector = Injector()

injector.add_ref(engine)
injector.add_com(Human)
injector.load()

car = injector.ref(Car)
print(car.info())

human = injector.ref(Human)
human.drive()
