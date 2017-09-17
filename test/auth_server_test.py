import pytest
import json
from os import environ
from clink.model.auth import res_bearer_token
from clink.model.acc import get_me_body
from clink.mime import MIME_JSON
from jsonschema import validate

_IS_TRAVIS = True if 'TRAVIS' in environ else False
_NEW_EMAIL = 'lily.tiger.000@yandex.com'
_NEW_USERNAME = 'lily-tiger-000'
_NEW_PASSWORD = 'secret-word'


def _req_token(auth_server):
    req_header = {'Content-Type': MIME_JSON}
    req_body = json.dumps({
        'grant_type': 'password',
        'username': auth_server.username,
        'password': auth_server.password
    })
    return auth_server.raw_post('/auth/token', req_header, req_body)


def _get_token(auth_server):
    res = _req_token(auth_server)
    assert res.status_code == 200
    return json.loads(res.text)


@pytest.mark.skipif('_IS_TRAVIS == True')
def test_reg_code(auth_server):
    req_header = {'Content-Type': MIME_JSON}
    req_body = json.dumps({
        'email': _NEW_EMAIL,
        'name': _NEW_USERNAME,
        'pwd': _NEW_PASSWORD
    })
    res = auth_server.raw_post('/acc/reg/code', req_header, req_body)
    assert res.status_code == 204


@pytest.mark.skipif('_IS_TRAVIS == True')
def test_put_pwd(auth_server):
    global _ROOT_PWD
    token = _get_token(auth_server)
    req_header = {
        'Content-Type': MIME_JSON,
        'Authorization': 'Bearer ' + token['access_token']
    }
    new_pwd = 'buffalow'
    req_body = json.dumps({
        'old_pwd': auth_server.password,
        'new_pwd': new_pwd
    })

    res = auth_server.raw_put('/acc/me/pwd', req_header, req_body)
    assert res.status_code == 204
    auth_server.password = new_pwd


@pytest.mark.skipif('_IS_TRAVIS == True')
def test_reset_pwd_code(auth_server):
    req_header = {'Content-Type': MIME_JSON}
    req_body = json.dumps({
        'email': auth_server.email
    })

    res = auth_server.raw_post('/acc/pwd/code', req_header, req_body)
    assert res.status_code == 204


@pytest.mark.skipif('_IS_TRAVIS == True')
def test_login(auth_server):
    '''
    Can not send email inside sandbox of travis-ci
    '''

    res_schema = {
        'body': res_bearer_token
    }

    res = _req_token(auth_server)
    assert res.status_code == 200

    res_body = json.loads(res.text)
    validate(res_body, res_schema)


@pytest.mark.skipif('_IS_TRAVIS == True')
def test_get_protected_res(auth_server):
    token = _get_token(auth_server)
    req_header = {
        'Authorization': 'Bearer ' + token['access_token']
    }

    res = auth_server.raw_get('/res/item', req_header)
    assert res.status_code == 200
    assert res.headers['Content-Type'] == MIME_JSON


@pytest.mark.skipif('_IS_TRAVIS == True')
def test_get_protected_res_failed(auth_server):
    res = auth_server.raw_get('/res/item')
    assert res.status_code == 401


@pytest.mark.skipif('_IS_TRAVIS == True')
def test_get_acc_info(auth_server):
    token = _get_token(auth_server)
    req_header = {
        'Authorization': 'Bearer ' + token['access_token']
    }

    res = auth_server.raw_get('/acc/me', req_header)
    assert res.status_code == 200
    res_body = json.loads(res.text)
    print(res_body)
    validate(res_body, get_me_body)


@pytest.mark.skipif('_IS_TRAVIS == True')
def test_get_acc_info_failed(auth_server):
    res = auth_server.raw_get('/acc/me')
    assert res.status_code == 401
