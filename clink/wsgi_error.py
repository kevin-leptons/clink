class WsgiResBodyError(Exception):
    def __init__(self, body):
        self.body = body

    def __str__(self):
        return 'response body of WSGI must bytes like object'
