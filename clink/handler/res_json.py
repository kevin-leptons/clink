'''
SYNOPSIS

    class ResJsonHandler

DESCRIPTION

    Encode object to JSON string. Use bson.json_util as encoder, output
    is strange. For example:

        o = {_id: ObjectId('5915e505e77989755d3cf4db')}

    After encode, result is:

        s = {"_id": {"$oid": "5915e505e77989755d3cf4db"}}
'''

from bson import json_util

from clink.iface import IPipeHandler
from clink.mime.type import MIME_JSON
from clink.etc import UTF_8
from clink.com import stamp
from clink.type.com import Lv5Handler


@stamp()
class ResJsonHandler(Lv5Handler):
    def handle(self, req, res):
        if res.content_type != MIME_JSON:
            return
        if res.body is None:
            return
        res.body = json_util.dumps(res.body).encode(UTF_8)
