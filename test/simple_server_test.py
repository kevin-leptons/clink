def test_api_info(simple_server):
    res_schema = {
        'body': {
            'type': 'object',
            'required': [
                'header', 'path', 'args', 'server_name',
                'server_port', 'server_protocol', 'content_length'
            ],
            'properties': {
                'header': {'type': 'object'},
                'path': {'type': 'string'},
                'args': {'type': 'object'},
                'server_name': {'type': 'string'},
                'server_port': {'type': 'number'},
                'server_protocol': {'type': 'string'},
                'content_length': {'type': 'number'},
            }
        }
    }
    simple_server.test_get('/api/info', res_schema=res_schema)


def test_http404(simple_server):
    simple_server.test_get('/not/exist/path', res_status=404)


def test_http405(simple_server):
    simple_server.test_post('/api/info', res_status=405)


def test_http500(simple_server):
    simple_server.test_get('/api/http500', res_status=500)
