from clink.mime import MIME_ICO


def test_get_root(simple_server):
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
    simple_server.test_get('/', res_schema=res_schema)


def test_http404(simple_server):
    simple_server.test_get('/status/404', res_status=404)


def test_http405(simple_server):
    simple_server.test_get('/status/405', res_status=405)


def test_http409(simple_server):
    simple_server.test_get('/status/409', res_status=409)


def test_http500(simple_server):
    simple_server.test_get('/status/500', res_status=500)


def test_get(simple_server):
    simple_server.test_get('/res/item', res_status=200)


def test_post(simple_server):
    simple_server.test_post('/res/item', res_status=200)


def test_put(simple_server):
    simple_server.test_put('/res/item', res_status=200)


def test_patch(simple_server):
    simple_server.test_patch('/res/item', res_status=200)


def test_delete(simple_server):
    simple_server.test_delete('/res/item', res_status=200)


def test_post_get(simple_server):
    simple_server.test_post('/res/get', res_status=405)


def test_get_post(simple_server):
    simple_server.test_get('/res/post', res_status=405)


def test_get_put(simple_server):
    simple_server.test_get('/res/put', res_status=405)


def test_get_patch(simple_server):
    simple_server.test_get('/res/patch', res_status=405)


def test_get_delete(simple_server):
    simple_server.test_get('/res/delete', res_status=405)


def test_invalid_content_type(simple_server):
    header = {'Content-Type': MIME_ICO}
    simple_server.test_post('/res/text', req_header=header, res_status=400)
