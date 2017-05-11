from .ihandler import IHandler


class ResCorsHandler(IHandler):
    def handle(self, req, res):
        if req.method.lower() != 'option':
            return
        res.header['Access-Control-Allow-Origin'] = '*'
        res.header['Access-Control-Allow-Methods'] = \
            'GET,POST,PUT,DELETE,OPTIONS'
        res.header['Access-Control-Allow-Headers'] = \
            'Authorization,Content-Type'
