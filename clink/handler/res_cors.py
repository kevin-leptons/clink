from clink.iface import IPipeHandler
from clink.com import stamp
from clink.type import Lv5Handler


@stamp()
class ResCorsHandler(Lv5Handler):
    def handle(self, req, res):
        if req.method.lower() != 'option':
            return
        res.header['Access-Control-Allow-Origin'] = '*'
        res.header['Access-Control-Allow-Methods'] = \
            'GET,POST,PUT,DELETE,OPTIONS'
        res.header['Access-Control-Allow-Headers'] = \
            'Authorization,Content-Type'
