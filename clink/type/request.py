class Request():
    method = None
    path = None
    query_str = None
    content_type = None
    content_length = None
    server_name = None
    server_port = None
    server_protocol = None
    remote_addr = None
    remote_port = None

    header = {}
    body = None

    args = {}

    def __init__(self):
        pass
