import json

from .http_error import Http400Error
from .ihandler import IHandler
from .encoding import UTF_8
from .mime_type import MIME_JSON


class ReqJsonHandler(IHandler):
    def handle(self, req, res):
        if req.content_type != MIME_JSON:
            return
        if req.body is None:
            return
        try:
            req.body = json.loads(req.body.decode(UTF_8))
        except ValueError:
            raise Http400Error(req, 'body is invalid json format')
