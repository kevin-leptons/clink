class Header(dict):
    pass


class Request():
    def __init__(self, method, path, header, body):
        self.path = path
        self.method = method
        self.header = header
        self.body = body

        self.params = {}
        self.args = {}


class Response():
    def __init__(self, status, header, body):
        self.status = status
        self.header = header
        self.body = body
