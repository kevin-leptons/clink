import json

from clink.error.http import code_to_str
from clink.iface import ILv7Handler
from clink.mime import MIME_JSON
from clink.com import stamp
from clink.dflow import ExistError, NonExistError, FormatError, ExpiredError


@stamp()
class DflowErrorHandler(ILv7Handler):
    '''
    Catch Data Flow error and make response message correspond with
    error
    '''

    def handle(self, req, res, e):
        if isinstance(e, ExistError):
            res.status = 409
            res.header = {}
            res.content_type = MIME_JSON
            res.body = json.dumps({
                'status': 409,
                'status_name': code_to_str(409),
                'message': e.indexes
            }).encode('utf-8')
            return True
        elif isinstance(e, NonExistError):
            res. status = 404
            res.header = {}
            res.content_type = MIME_JSON
            res.body = json.dumps({
                'status': 404,
                'status_name': code_to_str(404),
                'message': e.indexes
            }).encode('utf-8')
            return True
        elif isinstance(e, FormatError):
            res.status = 400
            res.header = {}
            res.content_type = MIME_JSON
            res.body = json.dumps({
                'status': 400,
                'status_name': code_to_str(400),
                'message': {
                    'name': e.name, 'value': str(e.value), 'schema': e.schema
                }
            }).encode('utf-8')
            return True
        elif isinstance(e, ExpiredError):
            res.status = 403
            res.header = {}
            res.content_type = MIME_JSON
            res.body = json.dumps({
                'status': 403,
                'status_name': code_to_str(403),
                'message': e.indexes
            }).encode('utf-8')
            return True
        else:
            return False
