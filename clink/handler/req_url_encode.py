from urllib.parse import parse_qsl

from ..error.http import Http400Error
from ..iface import IPipeHandler
from ..mime.type import MIME_URLENCODE


class ReqUrlEncodeHandler(IPipeHandler):
    def handle(self, req, res, ctx):
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
