import json
from urllib.parse import parse_qsl

from .http_error import Http400Error


def json_req_handle(req, res):
    if req.content_type != 'application/json':
        return
    if req.body is None:
        return
    try:
        req.body = json.loads(req.body.decode('utf-8'))
    except ValueError:
        raise Http400Error(req, 'body is invalid json format')


def form_req_handle(req, res):
    if req.content_type != 'application/x-www-form-urlencoded':
        return
    if req.body is None:
        return
    try:
        req.body = dict(parse_qsl(req.body.decode('utf-8')))
    except ValueError:
        raise Http400Error(req)
