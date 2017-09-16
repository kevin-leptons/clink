import json

from clink.error.http import Http400Error
from clink.iface import ILv3Handler
from clink.mime import MIME_JSON
from clink.com import stamp


@stamp()
class ReqJsonHandler(ILv3Handler):
    '''
    Map JSON string from body message to Python object
    '''

    def handle(self, req, res):
        if req.content_type != MIME_JSON:
            return
        if req.body is None:
            return
        try:
            req.body = json.loads(req.body.decode('utf-8'))
        except ValueError:
            raise Http400Error(req, 'body is invalid json format')
