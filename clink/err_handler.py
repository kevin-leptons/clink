import json

from .http_error import HttpError, code_to_str


def http_err_handler(req, res, e, wsgi_send):
    if not isinstance(e, HttpError):
        return
    res.status = e.status
    res.header = {}
    res.content_type = 'application/json'
    res.body = json.dumps({
        'status': e.status,
        'status_name': code_to_str(e.status),
        'message': e.msg
    })
