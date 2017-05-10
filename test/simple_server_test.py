def test_simple_server(simple_server):
    res_schema = {
        'body': {
            'type': 'object',
            'required': ['name', 'author'],
            'properties': {
                'name': {'type': 'string'},
                'authro': {'type': 'string'}
            }
        }
    }
    simple_server.test_get('/book/item', res_schema=res_schema)
