from pytest import mark

token = None
username = None
password = None
email = None


def test_register(auth_server, rand):
    username = rand.username()
    email = rand.email()
    password = rand.password()

    req_body = {
        'username': username,
        'email': email,
        'password': password
    }

    auth_server.test_post('/account/user', req_body=req_body, res_status=204)


def test_get_token_pwd(auth_server):
    req_body = {
        'username': username,
        'password': password
    }
    res_schema = {
        'body': {
            'type': 'object',
            'required': ['access_token', 'refresh_token', 'expires_in'],
            'properties': {
                'token_type': {'type': 'string', 'pattern': '^Bearer$'},
                'expires_in': {'type': 'number'},
                'access_token': {'type': 'string'},
                'refresh_token': {'type': 'string'}
            }
        }
    }

    auth_server.test_post(
        '/auth/token', req_body=req_body,
        res_status=200, res_schema=res_schema
    )


@mark.skip()
def test_get_me(auth_server):
    req_header = {
        'AUTHORIZATION': 'Bearer 123'
    }
    res_schema = {
        'body': {
            'username': {'type': 'string'}
        }
    }
    auth_server.test_get(
        '/account/me', req_header=req_header,
        res_status=200, res_schema=res_schema
    )
