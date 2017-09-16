from urllib.parse import parse_qsl

from clink.error.http import Http400Error
from clink.iface import ILv3Handler
from clink.mime import MIME_URLENCODE
from clink.com import stamp


@stamp()
class ReqUrlEncodeHandler(ILv3Handler):
    '''
    Map URL Encode string to Python object
    '''

    def handle(self, req, res):
        if req.content_type != MIME_URLENCODE:
            return
        if req.body is None:
            return
        try:
            values = dict(parse_qsl(req.body.decode('utf-8')))
            if req.body is not None and len(values) == 0:
                raise Http400Error(req, 'body is invaild url encode')
            req.body = values
        except ValueError:
            raise Http400Error(req)
