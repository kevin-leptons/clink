from os import path
from os.path import dirname, realpath
from datetime import datetime, timedelta

from jwt.exceptions import ExpiredSignatureError

from clink.error.http import Http401Error, Http404Error
from clink import stamp, mapper, AppConf, AuthConf, Controller
from clink.service import AccSv, TemplateSv, SmtpSv, OAuthSv

_DIR = realpath(path.join(dirname(__file__), '../tpl'))
_REG_CODE_TMP_FILE = path.join(_DIR, 'reg-code.txt')
_REG_TMP_FILE = path.join(_DIR, 'reg-tmp.txt')
_CHANGE_PWD_TMP_FILE = path.join(_DIR, 'change-pwd.txt')
_RESET_PWD_TMP_FILE = path.join(_DIR, 'reset-pwd.txt')
_RESET_PWD_CODE_TMP_FILE = path.join(_DIR, 'reset-pwd-code.txt')


@stamp(AppConf, AuthConf, AccSv, OAuthSv, SmtpSv, TemplateSv)
@mapper.path('acc')
class AccountCtl(Controller):
    '''
    POST /acc/reg/code
    POST /acc/reg

    GET  /acc/me
    PUT  /acc/me/pwd

    POST /acc/pwd/code
    POST /acc/pwd
    '''

    def __init__(
        self, app_conf, auth_conf, acc_sv, oauth_sv, smtp_sv, tpl_sv
    ):
        self._app_conf = app_conf
        self._auth_conf = auth_conf
        self._acc_sv = acc_sv
        self._oauth_sv = oauth_sv
        self._smtp_sv = smtp_sv
        self._tpl_sv = tpl_sv

    @mapper.get('me')
    def get_me(self, req, res):
        try:
            acc_id = self._oauth_sv.authen_req(req)
            acc = self._acc_sv.find_id(acc_id)
            if acc is None:
                raise Http404Error(req, 'Identity %s invalid' % str(acc_id))

            res.body = {
                '_id': str(acc['_id']),
                'name': acc['name'],
                'email': acc['email'],
                'phone': acc['phone'],
                'created_date': int(acc['created_date'].timestamp()),
                'modifired_date': int(acc['modified_date'].timestamp()),
                'last_action': acc['last_action']
            }
        except ExpiredSignatureError:
            raise Http401Error(req, 'Token was expired')

    @mapper.post('reg/code')
    def create_reg_code(self, req, res):
        info = req.body

        reg_code = self._acc_sv.mk_reg_code(
            info['name'], info['pwd'], info['email']
        )

        datetime_now = datetime.utcnow()
        expired_date = datetime_now + timedelta(self._acc_sv.create_time)
        values = {
            'reg_code': reg_code,
            'acc_name': info['name'],
            'acc_email': info['email'],
            'expired_date': expired_date.strftime('%Y-%m-%d %H:%M:%S'),
            'remote_addr': req.remote_addr
        }
        txt_body = self._tpl_sv.build_file(_REG_CODE_TMP_FILE, values)
        subject = 'Registration'
        self._smtp_sv.send(info['email'], subject, txt_body)

        res.status = 204

    @mapper.post('reg')
    def confirm_reg_code(self, req, res):
        reg_code = req.body['code']

        acc = self._acc_sv.cf_reg_code(reg_code)

        values = {
            'acc_name': acc['name'],
            'acc_email': acc['email'],
            'remote_addr': req.remote_addr
        }
        txt_body = self._tpl_sv.build_file(_REG_TMP_FILE, values)
        subject = 'Registration'
        self._smtp_sv.send(acc['email'], subject, txt_body)

        res.status = 204

    @mapper.put('me/pwd')
    def change_pwd(self, req, res):
        try:
            new_pwd = req.body['new_pwd']

            acc_id = self._oauth_sv.authen_req(req)
            acc = self._acc_sv.find_id(acc_id)
            if acc is None:
                raise Http404Error(req, 'Not fuond identity %s' % str(acc_id))
            self._acc_sv.ch_pwd(acc_id, new_pwd)

            values = {
                'acc_name': acc['name'],
                'remote_addr': req.remote_addr
            }
            txt_body = self._tpl_sv.build_file(_CHANGE_PWD_TMP_FILE, values)
            subject = 'Change password'
            self._smtp_sv.send(acc['email'], subject, txt_body)

            res.status = 204
        except ExpiredSignatureError:
            raise Http401Error(req, 'Token was expired')

    @mapper.post('pwd/code')
    def create_reset_pwd_code(self, req, res):
        email = req.body['email']

        acc = self._acc_sv.find_email(email)
        if acc is None:
            raise Http404Error(req, 'Email does not exist')

        reset_code = self._acc_sv.mk_rpwd_code(email)
        expired_date = datetime.utcnow() + timedelta(hours=1)

        values = {
            'reset_pwd_code': reset_code,
            'app_name': self._app_conf.name,
            'acc_name': acc['name'],
            'expired_date': expired_date.strftime('%Y-%m-%d %H:%M:%S'),
            'remote_addr': req.remote_addr
        }

        txt_body = self._tpl_sv.build_file(_RESET_PWD_CODE_TMP_FILE, values)
        subject = 'Reset password code'
        self._smtp_sv.send(email, subject, txt_body)

        res.status = 204

    @mapper.post('pwd')
    def confirm_reset_pwd_code(self, req, res):
        reset_code = req.body['code']
        new_pwd = req.body['new_pwd']

        acc_id = self._acc_sv.cf_rpwd_code(reset_code, new_pwd)

        acc = self._acc_sv.find_id(acc_id)
        if acc is None:
            raise Http404Error(req, 'Not found identity %s' % str(acc_id))

        values = {
            'new_pwd': new_pwd,
            'reset_pwd_code': reset_code,
            'acc_name': acc['name'],
            'remote_addr': req.remote_addr
        }

        txt_msg = self._tpl_sv.build_file(_RESET_PWD_TMP_FILE, values)
        subject = 'Reset password'
        self._smtp_sv.send(acc['email'], subject, txt_msg)

        res.status = 204
