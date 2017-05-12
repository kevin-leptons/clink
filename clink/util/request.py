from ..error.http import Http403Error, Http413Error


def accept_remote(remotes):
    def decorator_fn(target_fn):
        def handle(req, res):
            if req.remote_addr not in remotes:
                raise Http403Error(req)
            target_fn(req, res)
        return handle
    return decorator_fn


def denie_remote(remotes):
    def decorator_fn(target_fn):
        def handle(req, res):
            if req.remote_addr in remotes:
                raise Http403Error(req)
            target_fn(req, res)
        return handle
    return decorator_fn


def accept_size(min, max):
    def decorator_fn(target_fn):
        def handle(req, res):
            if req.content_length < min or req.content_length > max:
                raise Http413Error(req)
            target_fn(req, res)
        return handle
    return decorator_fn
