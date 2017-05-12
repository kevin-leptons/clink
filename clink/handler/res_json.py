import json

from ..iface import IPipeHandler
from ..mime.type import MIME_JSON
from ..etc import UTF_8


class ResJsonHandler(IPipeHandler):
    def handle(self, req, res):
        if res.content_type != MIME_JSON:
            return
        if res.body is None:
            return
        res.body = json.dumps(res.body).encode(UTF_8)
