import json


def json_res_handle(req, res):
    if res.content_type != 'application/json':
        return
    if res.body is None:
        return
    res.body = json.dumps(res.body)


def cors_res_handle(req, res):
    if req.method.lower() != 'option':
        return
    res.header['Access-Control-Allow-Origin'] = '*'
    res.header['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    res.header['Access-Control-Allow-Headers'] = 'Authorization,Content-Type'
