from bson import json_util

from clink.iface import ILv5Handler
from clink.mime import MIME_JSON
from clink.com import stamp


@stamp()
class ResJsonHandler(ILv5Handler):
    '''
    Serialize Python object to JSON string
    '''

    def handle(self, req, res):
        if res.content_type != MIME_JSON:
            return
        if res.body is None:
            return
        res.body = json_util.dumps(res.body).encode('utf-8')
