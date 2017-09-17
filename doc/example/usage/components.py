from clink.com import Component, Injector, stamp
from clink.type import Request, Response


# this is component
@stamp()
class AccountService(Component):
    def create(self, info):
        print('created:', info)


# this other component
@stamp(AccountService)
class AccountCtl(Component):
    def __init__(self, account_service):
        # this is dependency
        self._account_service = account_service

    # this is component's function
    def create(self, req, res):
        info = req.body
        self._account_service.create(info)


# this is injector
i = Injector()


# add component into injector
i.add_com(AccountCtl)


# this is auto creation, dependency solving
i.load()


# this is getting instances
acc_ctl = i.ref(AccountCtl)


# try call function
req = Request()
res = Response()
req.body = {'name': 'Micheal', 'email': 'michael@mars.com'}
acc_ctl.create(req, res)


# get other instace
acc_sv = i.ref(AccountService)
print(acc_sv)
