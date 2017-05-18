from clink.com.type import Component
from clink.com.marker import com


@com()
class AppConfig(Component):
    def __init__(self, name, dburl=None):
        self.name = name
        self.dburl = dburl
