import json

from ..error.http import Http400Error
from ..iface import IPipeHandler
from ..etc import UTF_8
from ..mime.type import MIME_JSON


class ReqJsonHandler(IPipeHandler):
    def handle(self, req, res, ctx):
        if req.content_type != MIME_JSON:
            return
        if req.body is None:
            return
        try:
            req.body = json.loads(req.body.decode(UTF_8))
        except ValueError:
            raise Http400Error(req, 'body is invalid json format')
