from .wsgi_error import WsgiResBodyError
from .http_error import code_to_str
from .ihandler import ISendHandler


class SendHandler(ISendHandler):
    def handle(self, req, res, wsgi_send):
        header = [(k, v) for k, v in res.header.items()]
        if res.content_type is not None:
            header.append(('Content-Type', res.content_type))
        if res.body is None:
            return []
        elif not isinstance(res.body, bytes):
            raise WsgiResBodyError(res.body)
        else:
            wsgi_send(code_to_str(res.status), header)
            return [res.body]
