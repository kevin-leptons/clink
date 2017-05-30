from clink.com import stamp, Injector, Component


@stamp()
class Pump(Component):
    def run(self):
        print('Pump was started')


@stamp(Pump)
class Nozzle(Component):
    def __init__(self, pump):
        self._pump = pump

    def spray(self):
        self._pump.run()
        print('Nozzle is spraying')


injector = Injector()
injector.add_com(Nozzle)
injector.load()

nozzle = injector.ref(Nozzle)
nozzle.spray()
