import json

from clink.error.http import code_to_str
from clink.iface import ILv7Handler
from clink.mime import MIME_JSON
from clink.com import stamp
from clink.routing.error import PathNotFoundError, HandleNotFoundError


@stamp()
class RoutingErrorHandler(ILv7Handler):
    '''
    Catch routing error and send information to client
    '''

    def handle(self, req, res, e):
        if isinstance(e, PathNotFoundError):
            res.status = 404
            res.header = {}
            res.content_type = MIME_JSON
            res.body = json.dumps({
                'status': 404,
                'status_name': code_to_str(404),
                'message': 'Path does not exist'
            }).encode('utf-8')
            return True
        elif isinstance(e, HandleNotFoundError):
            res.status = 405
            res.header = {}
            res.content_type = MIME_JSON
            res.body = json.dumps({
                'status': 405,
                'status_name': code_to_str(405),
                'message': 'No handler for method'
            }).encode('utf-8')
            return True

        return False
