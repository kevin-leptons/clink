import json

from .mime_type import MIME_JSON


def json_res_handle(req, res):
    if res.content_type != MIME_JSON:
        return
    if res.body is None:
        return
    res.body = json.dumps(res.body).encode('utf-8')


def cors_res_handle(req, res):
    if req.method.lower() != 'option':
        return
    res.header['Access-Control-Allow-Origin'] = '*'
    res.header['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    res.header['Access-Control-Allow-Headers'] = 'Authorization,Content-Type'
