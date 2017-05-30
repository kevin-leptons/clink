from lib.auth_app import ROOT_PWD
from clink.model.auth import res_bearer_token


def test_login(auth_server):
    req_body = {
        'grant_type': 'password',
        'username': 'root',
        'password': ROOT_PWD
    }
    res_schema = {
        'body': res_bearer_token
    }

    auth_server.test_post(
        '/auth/token', req_body=req_body,
        res_status=200, res_schema=res_schema
    )
