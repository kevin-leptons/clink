import json

from clink.error.http import HttpError, code_to_str
from clink.iface import ILv7Handler
from clink.mime import MIME_JSON
from clink.com import stamp


@stamp()
class ErrorHttpHandler(ILv7Handler):
    '''
    Catch HTTP error and make response message correspond with
    error
    '''

    def handle(self, req, res, e):
        if not isinstance(e, HttpError):
            return False
        res.status = e.status
        res.header = {}
        res.content_type = MIME_JSON
        res.body = json.dumps({
            'status': e.status,
            'status_name': code_to_str(e.status),
            'message': e.msg
        }).encode('utf-8')
        return True
