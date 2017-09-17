import json
import requests
from time import time
from requests import post, Request, Session
from urllib.parse import urljoin, urlencode
from jsonschema import validate


class Invoker():
    '''
    Provide shortcut way to test http api

    :param string host: Hostname or IP address
    :param string oauth_endpoint: Endpoint of oauth-2
    :param string username: Username for oauth-2
    :param string password: Password for oauht-2
    '''

    def __init__(
        self, host,
        oauth_endpoint=None, username=None, password=None, email=None
    ):
        self._host = host
        self._oauth_endpoint = oauth_endpoint
        self._username = username
        self.password = password
        self._email = email

        # mark access_token never is retrieve
        self._token = None
        self._token_expired = 0

        # session use to send request
        self._session = Session()

    @property
    def username(self):
        return self._username

    @property
    def email(self):
        return self._email

    def raw_get(self, path, header=None):
        return requests.get(self.url(path), headers=header)

    def raw_post(self, path, header=None, body=None):
        return requests.post(self.url(path), headers=header, data=body)

    def raw_put(self, path, header=None, body=None):
        return requests.put(self.url(path), headers=header, data=body)

    def raw_patch(self, path, header=None, body=None):
        return requests.patch(self.url(path), headers=header, data=body)

    def raw_delete(self, path, header=None, body=None):
        return requests.patch(self.url(path), headers=header, data=body)

    def test_get(
        self, path,
        *, auth=False, req_header=None, res_status=200, res_schema=None
    ):
        '''
        Test api with GET method

        :param string path: Path to do test
        :param boolean auth: If true, include access token in request header
            to Authoriztion key
        :param dict req_header: Header include to request message.
            Authorization value will be override if auth parameter is True
        :param int res_status: Expected response status
        :param dict res_schema: Json schema is expected to response message
        '''

        self._test(
            'GET', path=path, auth=auth, req_header=req_header,
            res_status=res_status, res_schema=res_schema
        )

    def test_post(
        self, path,
        *, auth=False, req_header=None, req_body=None,
        res_status=204, res_schema=None
    ):
        '''
        Test api with POST method

        :param string path: Path to do test
        :param boolean auth: If true, include access token in request header
            to Authoriztion key
        :param dict req_header: Header include to request message.
            Authorization value will be override if auth parameter is True
        :param req_body: Request body, can be string or dict
        :param int res_status: Expected response status
        :param dict res_schema: Json schema is expected to response message
        '''
        self._test(
            'POST', path=path, auth=auth,
            req_header=req_header, req_body=req_body,
            res_status=res_status, res_schema=res_schema
        )

    def test_put(
        self, path,
        *, auth=False, req_header=None, req_body=None,
        res_status=204, res_schema=None
    ):
        '''
        Test api with PUT method

        :param string path: Path to do test
        :param boolean auth: If true, include access token in request header
            to Authoriztion key
        :param dict req_header: Header include to request message.
            Authorization value will be override if auth parameter is True
        :param req_body: Request body, can be string or dict
        :param int res_status: Expected response status
        :param dict res_schema: Json schema is expected to response message
        '''
        self._test(
            'PUT', path=path, auth=auth,
            req_header=req_header, req_body=req_body,
            res_status=res_status, res_schema=res_schema
        )

    def test_patch(
        self, path,
        *, auth=False, req_header=None, req_body=None,
        res_status=204, res_schema=None
    ):
        '''
        Test api with PUT method

        :param string path: Path to do test
        :param boolean auth: If true, include access token in request header
            to Authoriztion key
        :param dict req_header: Header include to request message.
            Authorization value will be override if auth parameter is True
        :param req_body: Request body, can be string or dict
        :param int res_status: Expected response status
        :param dict res_schema: Json schema is expected to response message
        '''
        self._test(
            'PATCH', path=path, auth=auth,
            req_header=req_header, req_body=req_body,
            res_status=res_status, res_schema=res_schema
        )

    def test_delete(
        self, path,
        *, auth=False, req_header=None,
        res_status=204, res_schema=None
    ):
        '''
        Test api with DELETE method

        :param string path: Path to do test
        :param boolean auth: If true, include access token in request header
            to Authoriztion key
        :param dict req_header: Header include to request message.
            Authorization value will be override if auth parameter is True
        :param int res_status: Expected response status
        :param dict res_schema: Json schema is expected to response message
        '''
        self._test(
            'DELETE', path=path, auth=auth,
            req_header=req_header,
            res_status=res_status, res_schema=res_schema
        )

    def _test(
        self, method, path,
        *, auth=False, req_header=None, req_body=None,
        res_status=200, res_schema=None
    ):
        '''
        Test api with custom request

        :param string method: Http method GET, POST, PUT,
            PATCH, DELETE
        :param string path: Path to do test
        :param boolean auth: If true, include access token in request header
            to Authoriztion key
        :param dict req_header: Header include to request message.
            Authorization value will be override if auth parameter is True
        :param req_body: Request body, can be string or dict
        :param int res_status: Expected response status
        :param dict res_schema: Json schema is expected to response message
        '''

        # prepare request header
        if req_header is None:
            req_header = {}
        if auth is True:
            bearer = 'Bearer {}'.format(self.access_token())
            req_header['Authorization'] = bearer

        # prepare encoded body
        encoded_body = None
        if 'Content-Type' not in req_header:
            req_header['Content-Type'] = 'application/json'
        if req_body is not None:
            content_type = req_header['Content-Type']

            if content_type == 'application/json':
                encoded_body = json.dumps(req_body)
            elif content_type == 'application/x-www-form-urlencoded':
                encoded_body = urlencode(req_body)
            else:
                encoded_body = req_body

        # prepare request message
        req = Request(
            method, self.url(path),
            headers=req_header, data=encoded_body
        )
        prepped = req.prepare()

        # perform request
        res = self._session.send(prepped)

        # validate response status
        if res.status_code != res_status:
            self._raise('Status code is not equal {}'.format(res_status), res)

        # validate response message
        if res_schema is not None:
            if 'header' in res_schema and res_schema['header'] is not None:
                validate(dict(res.headers), res_schema['header'])
            if 'body' in res_schema and res_schema['body'] is not None:
                validate(res.json(), res_schema['body'])
            if 'header' not in res_schema and 'body' not in res_schema:
                raise RuntimeError('Response schema is invalid')

    def url(self, path):
        '''
        Get url by join host with path

        :param string path: Relative path
        :return: Url
        :rtype: string
        '''

        return urljoin(self._host, path)

    def get_token(self):
        '''
        Get token from username and password. It use oauth-2,
        grant_type = password

        :return: token
        :rtype: dict
        '''

        # token is early exist, and it is not expired
        now = int(time())
        if self._token_expired > 0 and self._token_expired > now:
            return self._token

        # re invoke token
        req_body = {
            'grant_type': 'password',
            'username': self._username,
            'password': self._password
        }
        res = post(self.url(self._oauth_endpoint), data=req_body)

        # verify response
        if res.status_code != 200:
            self._raise('Can not authenticate with service oauth-2', res)
        token = res.json()
        if 'access_token' not in token:
            self._raise('Response have not access_token field', res)
        if 'expires_in' not in token:
            self._raise('Response have not expires_in field', res)

        # save token
        self._token = token
        self._token_expired = now + int(token['expires_in'])

        return self._token

    def access_token(self):
        '''
        Get access token

        :return: access_token
        :rtype: str
        '''
        return self.get_token()['access_token']

    def refresh_token(self):
        '''
        Get fresh token

        :return: refresh_token
        :rtype: str
        '''

        return self.get_token()['refresh_token']

    def _raise(self, title, res):
        '''
        Raise error from response message

        :param str title: Error title
        :param requests.Response: Response message
        '''

        msg = title
        msg += '; Status code: {}'.format(res.status_code)
        msg += '; {}'.format(res.text)

        raise RuntimeError(msg)
