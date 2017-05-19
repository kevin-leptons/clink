import clink

from clink import com
from clink.type.com import Controller
from clink.ske.auth import ctl


class App(clink.App):
    def __init__(self, app_conf, mongo_conf, auth_conf):
        super().__init__(app_conf)

        self.injector.add_inst(mongo_conf)
        self.injector.add_inst(auth_conf)

        ctl_coms = com.find(ctl, Controller)
        self.injector.add_coms(ctl_coms)
