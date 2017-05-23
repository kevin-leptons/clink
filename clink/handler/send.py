from clink.error.wsgi import WsgiResBodyError
from clink.error.http import code_to_str
from clink.iface import ISendHandler
from clink.com import stamp
from clink.type import Lv6Handler


@stamp()
class SendHandler(Lv6Handler, ISendHandler):
    def handle(self, req, res, wsgi_send):
        if res.body is not None and not isinstance(res.body, bytes):
            raise WsgiResBodyError(res.body)

        header = [(k, v) for k, v in res.header.items()]
        if res.content_type is not None:
            header.append(('Content-Type', res.content_type))
        wsgi_send(code_to_str(res.status), header)

        if res.body is None:
            return []
        else:
            return [res.body]
