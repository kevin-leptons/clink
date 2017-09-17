from clink.com import Injector, Component, Primitive, stamp


@stamp()
class Engine(Primitive):
    def __init__(self, name):
        self.name = name


@stamp(Engine)
class Car(Component):
    def __init__(self, engine):
        self.engine = engine

    def info(self):
        return 'A car with %s engine' % self.engine.name


@stamp(Car)
class Human(Component):
    def __init__(self, car):
        self.car = car

    def drive(self):
        print('I drive %s' % self.car.info())


engine = Engine('Turbo v8')
injector = Injector()

injector.add_prim(engine)
injector.add_com(Human)
injector.load()

car = injector.ref(Car)
print(car.info())

human = injector.ref(Human)
human.drive()
