def test_simple_server(simple_server):
    res_schema = {
        'body': {
            'type': 'object',
            'required': [
                'header', 'path', 'args', 'server_name',
                'server_port', 'server_protocol', 'content_type',
                'content_length'
            ],
            'properties': {
                'header': {'type': 'object'},
                'path': {'type': 'string'},
                'args': {'type': 'object'},
                'server_name': {'type': 'string'},
                'server_port': {'type': 'number'},
                'server_protocol': {'type': 'string'},
                'content_type': {'type': 'string'},
                'content_length': {'type': 'number'},
            }
        }
    }
    simple_server.test_get('/api/info', res_schema=res_schema)
