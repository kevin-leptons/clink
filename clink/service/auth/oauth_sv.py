'''
SYNOPSIS

    class OAuth

DESCRIPTION

    Parts of OAuth2 authentication and authorization. It doesn't support all
    of OAuth2 specification, here are supported:

        RFC 6749, section 4.3 -  Resource Owner Password Credentials Grant

        RFC 6749, section 6 - Refreshing an Access Token

        RFC 7519 - JSON Web Token

    Other specifications isn't supported because it's complicated without
    browsers. For example, mobile device need polls auth server to gets token
    instead of gets it from auth provider directly.

    Use this limited OAuth specification, you can perform external login
    with other OAuth Provider, you can only use name-password to get
    token and refresh that token. However, it work on all of platform.

    It also ignore authorization 'scope'. Authorization is perform by
    query database, not by information in access_token.

REFERENCES

    RFC 6749 - OAuth 2.0 Framework
        https://tools.ietf.org/html/rfc6749

    RFC 6750 - Bearer Token Usage
        https://tools.ietf.org/html/rfc6750

    RFC 6819 - Threat Model and Security Considerations
        https://tools.ietf.org/html/rfc6819

    RFC 7519 - JSON Web Token
        https://tools.ietf.org/html/rfc7519

    OAuth Home Page
        https://oauth.net/2/
'''

import jwt
from time import time
from bson import ObjectId

from clink.com import com
from clink.type.com import Service
from clink.service.mongo import MongoService
from clink.error.http import Http400Error, Http401Error

from .error import AccountNotExist, PasswordError, TokenExpiredError, \
                   RTokenExpiredError
from .authdb_sv import AuthDbService
from .type import AuthConf
from .util import hash_pwd


@com(MongoService, AuthDbService, AuthConf)
class OAuthService(Service):
    _TOKEN_ALG = 'HS512'

    def __init__(self, mongo_sv, authdb_sv, auth_conf):
        pass
        self._acc_doc = mongo_sv.doc('account')
        self._grp_doc = mongo_sv.doc('group')

        self._jwt_key = auth_conf.jwt_key
        self._token_time = auth_conf.token_time
        self._rtoken_time = auth_conf.rtoken_time

    def mktoken_pwd(self, name, password):
        acc = self._acc_doc.find_one({'name': name})
        if acc is None:
            raise AccountNotExist(name)

        hashpwd = hash_pwd(password)
        if hashpwd != acc['hashpwd']:
            raise PasswordError(name, password)

        return self._mktoken(acc['_id'])

    def mktoken_rtoken(self, rtoken):
        rtoken_raw = jwt.decode(
            rtoken, self._jwt_key, algorithm=self._TOKEN_ALG
        )
        if rtoken_raw['exp'] < time():
            raise RTokenExpiredError(rtoken_raw)

        return self._mktoken(rtoken_raw['sub'])

    def authen(self, access_token):
        atoken_raw = jwt.decode(
            access_token, self._jwt_key, algorithm=self._TOKEN_ALG
        )
        exp = int(atoken_raw['exp'])
        if exp < time():
            raise TokenExpiredError(atoken_raw)

        return ObjectId(atoken_raw['sub'])

    def _mktoken(self, acc_id):
        return {
            'token_type': 'Bearer',
            'expires_in': time() + self._token_time,
            'access_token': self._mkatoken(acc_id),
            'refresh_token': self._mkrtoken(acc_id)
        }

    def _mkatoken(self, acc_id):
        token_raw = {
            'sub': str(acc_id),
            'exp': time() + self._token_time
        }
        token = jwt.encode(
            token_raw, self._jwt_key, algorithm=self._TOKEN_ALG
        )
        return token.decode()

    def _mkrtoken(self, acc_id):
        token_raw = {
            'sub': str(acc_id),
            'exp': time() + self._rtoken_time
        }
        token = jwt.encode(
            token_raw, self._jwt_key, algorithm=self._TOKEN_ALG
        )
        return token.decode()

    def authen_req(self, req):
        if 'AUTHORIZATION' not in req.header:
            raise Http401Error(req)
        auth_header = req.header['AUTHORIZATION']
        auth_type = auth_header[:7]
        if auth_type != 'Bearer ':
            raise Http400Error(req)
        atoken = auth_header[7:]

        return self.authen(atoken)
