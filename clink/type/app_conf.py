from clink.com.type import Component
from clink.com.marker import com


@com()
class AppConf(Component):
    def __init__(self, name, org_name, org_loc):
        self.name = name
        org_name = org_name
        org_loc = org_loc
