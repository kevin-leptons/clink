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

from ..iface import IPipeHandler
from ..mime.type import MIME_JSON
from ..etc import UTF_8


class ResJsonHandler(IPipeHandler):
    def handle(self, req, res, ctx):
        if res.content_type != MIME_JSON:
            return
        if res.body is None:
            return
        res.body = json_util.dumps(res.body).encode(UTF_8)
