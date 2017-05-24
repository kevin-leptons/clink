import clink

from clink import Controller
from clink.com import find
from clink.ske.auth import ctl


class App(clink.App):
    def __init__(self, app_conf, mongo_conf, auth_conf):
        super().__init__(app_conf)

        self.injector.add_ref(mongo_conf)
        self.injector.add_ref(auth_conf)

        ctl_coms = find(ctl, Controller)
        self.injector.add_coms(ctl_coms)
