from ..error.http import Http403Error, Http413Error


def remote(*args):
    def decorator_fn(target_fn):
        def handle(self, req, res):
            if req.remote_addr not in args:
                raise Http403Error(req)
            target_fn(self, req, res)
        return handle
    return decorator_fn


def denie_remote(*args):
    def decorator_fn(target_fn):
        def handle(self, req, res):
            if req.remote_addr in args:
                raise Http403Error(req)
            target_fn(self, req, res)
        return handle
    return decorator_fn


def max_content_size(max):
    def decorator_fn(target_fn):
        def handle(self, req, res):
            if req.content_length > max:
                raise Http413Error(req)
            target_fn(self, req, res)
        return handle
    return decorator_fn
