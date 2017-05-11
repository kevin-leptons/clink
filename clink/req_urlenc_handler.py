from urllib.parse import parse_qsl

from .http_error import Http400Error
from .ihandler import IHandler
from .mime_type import MIME_URLENCODE


class ReqUrlEncHandler(IHandler):
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
