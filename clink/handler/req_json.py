import json

from clink.error.http import Http400Error
from clink.iface import IPipeHandler
from clink.etc import UTF_8
from clink.mime.type import MIME_JSON
from clink.com.marker import com
from clink.type.com import Lv3Handler


@com()
class ReqJsonHandler(Lv3Handler, IPipeHandler):
    def handle(self, req, res):
        if req.content_type != MIME_JSON:
            return
        if req.body is None:
            return
        try:
            req.body = json.loads(req.body.decode(UTF_8))
        except ValueError:
            raise Http400Error(req, 'body is invalid json format')
