import json

from .ihandler import IHandler
from .mime_type import MIME_JSON
from .encoding import UTF_8


class ResJsonHandler(IHandler):
    def handle(self, req, res):
        if res.content_type != MIME_JSON:
            return
        if res.body is None:
            return
        res.body = json.dumps(res.body).encode(UTF_8)
