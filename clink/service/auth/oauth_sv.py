import jwt
from time import time
from bson import ObjectId
from jwt.exceptions import ExpiredSignatureError, DecodeError

from clink.type import AuthConf
from clink.com import stamp
from clink.type.com import Service
from clink.error.http import Http400Error, Http401Error
from clink.dflow import verify, NonExistError, ExpiredError, FormatError

from .authdb_sv import AuthDbSv
from .acc_sv import AccSv
from clink.model.std import acc_name as acc_name_model, acc_pwd as pwd_model


@stamp(AuthDbSv, AccSv, AuthConf)
class OAuthSv(Service):
    '''
    Limited OAuth2 implementation
    '''

    _TOKEN_ALG = 'HS512'

    def __init__(self, authdb_sv, acc_sv, auth_conf):
        '''
        :param AuthDbSv authdb_sv:
        :param AccSv acc_sv:
        :param AuthConf auth_conf:
        '''

        self._authdb_sv = authdb_sv
        self._acc_sv = acc_sv

        self._jwt_key = auth_conf.jwt_key
        self._token_time = auth_conf.token_time
        self._rtoken_time = auth_conf.rtoken_time

    @verify(None, acc_name_model, pwd_model)
    def mktoken_pwd(self, name, password):
        '''
        Create an token from account name and password

        :param str name:
        :param str password:
        :rtype: dict
        :raise NonExistError:
        '''

        acc = self._acc_sv.find_pwd(name, password)
        if acc is None:
            raise NonExistError({'name': name, 'password': '***'})

        return self._mk_token(acc['_id'])

    def mktoken_rtoken(self, rtoken):
        '''
        Create an token from refresh token

        :param str rtoken:
        :rtype: dict
        :raise TypeError:
        :raise ExpiredError:
        '''

        try:
            rtoken_raw = jwt.decode(
                rtoken, self._jwt_key, algorithm=self._TOKEN_ALG
            )
            return self._mk_token(rtoken_raw['sub'])
        except ExpiredSignatureError:
            raise ExpiredError({'refresh_token': None})
        except DecodeError:
            raise FormatError('refresh_token', None, None)

    def authen(self, access_token):
        '''
        Authenticate access token

        :param str access_token:
        :rtype: bson.objectid.ObjectId
        :raise FormatError:
        :raise ExpiredError:
        '''

        try:
            atoken_raw = jwt.decode(
                access_token, self._jwt_key, algorithm=self._TOKEN_ALG
            )
            return ObjectId(atoken_raw['sub'])
        except ExpiredSignatureError:
            raise ExpiredError({'access_token': None})
        except DecodeError:
            raise FormatError('access_token', None, None)

    def authen_req(self, req):
        '''
        Authenticate HTTP request

        :param Request req:
        :rtype mongo.objectid.ObjectId:
        :raise Http400Error:
        '''

        if 'AUTHORIZATION' not in req.header:
            raise Http401Error(req)
        auth_header = req.header['AUTHORIZATION']
        auth_type = auth_header[:7]
        if auth_type != 'Bearer ':
            raise Http400Error(req)
        atoken = auth_header[7:]

        return self.authen(atoken)

    def _mk_token(self, acc_id):
        '''
        Create token

        :param bson.objectid.ObjectId:
        :rtype: dict
        '''

        return {
            'token_type': 'Bearer',
            'expires_in': time() + self._token_time,
            'access_token': self._mk_atoken(acc_id),
            'refresh_token': self._mk_rtoken(acc_id)
        }

    def _mk_atoken(self, acc_id):
        '''
        Create access token

        :param bson.object.ObjectId:
        :rtype: str
        '''

        token_raw = {
            'sub': str(acc_id),
            'exp': time() + self._token_time
        }
        token = jwt.encode(
            token_raw, self._jwt_key, algorithm=self._TOKEN_ALG
        )
        return token.decode()

    def _mk_rtoken(self, acc_id):
        '''
        Create refresh token

        :param bson.object.ObjectId:
        :rtype: str
        '''

        token_raw = {
            'sub': str(acc_id),
            'exp': time() + self._rtoken_time
        }
        token = jwt.encode(
            token_raw, self._jwt_key, algorithm=self._TOKEN_ALG
        )
        return token.decode()
