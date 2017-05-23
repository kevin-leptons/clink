from clink.iface import ILv5Handler
from clink.com import stamp


@stamp()
class ResCorsHandler(ILv5Handler):
    '''
    Inform client to know that server allow CORS
    '''

    def handle(self, req, res):
        if req.method.lower() != 'option':
            return
        res.header['Access-Control-Allow-Origin'] = '*'
        res.header['Access-Control-Allow-Methods'] = \
            'GET,POST,PUT,DELETE,OPTIONS'
        res.header['Access-Control-Allow-Headers'] = \
            'Authorization,Content-Type'
