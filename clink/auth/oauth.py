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

from .error import AccountNotExist, PasswordError, TokenExpiredError, \
                   RTokenExpiredError
from .util import hash_pwd


class OAuth():
    _TOKEN_ALG = 'HS512'

    def __init__(
        self, acc_doc, grp_doc, jwt_key,
        token_time=4*3600, rtoken_time=30*24*3600
    ):
        self._acc_doc = acc_doc
        self._grp_doc = grp_doc
        self._jwt_key = jwt_key
        self._token_time = token_time
        self._rtoken_time = rtoken_time

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
