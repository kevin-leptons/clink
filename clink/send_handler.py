from .http_error import code_to_str


def send_handler(req, res, wsgi_send):
    header = [(k, v) for k, v in res.header.items()]
    if res.content_type is not None:
        header.append(('Content-Type', res.content_type))
    wsgi_send(code_to_str(res.status), header)
