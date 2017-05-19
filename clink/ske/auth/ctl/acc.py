'''
SYNOPSIS

    POST /acc/reg/code
    POST /acc/reg

    GET  /acc/me
    PUT  /acc/me/pwd

    POST /acc/pwd/code
    POST /acc/pwd

DESCRIPTION

    Create code for registration. Confirm registration code to active account.

    Get information of account.

    Change password.

    Create code for reset password. Confirm reset password code and new
    password to reset password.
'''

from os import path
from os.path import dirname, realpath
from datetime import datetime, timedelta
from bson import ObjectId

from clink.error.http import Http401Error, Http400Error, Http500Error, \
                      Http404Error
from clink.service.auth import AccService, AuthConf
from clink.service.template import build_tpl
from clink.com.marker import com
from clink.marker import route
from clink.type.com import Controller
from clink.service.mail import SmtpService
from clink.service.auth import OAuthService
from clink.type import AppConf

_DIR = realpath(path.join(dirname(__file__), '../tpl'))
_REG_CODE_TMP_FILE = path.join(_DIR, 'reg-code.txt')
_REG_TMP_FILE = path.join(_DIR, 'reg-tmp.txt')
_CHANGE_PWD_TMP_FILE = path.join(_DIR, 'change-pwd.txt')
_RESET_PWD_TMP_FILE = path.join(_DIR, 'reset-pwd.txt')
_RESET_PWD_CODE_TMP_FILE = path.join(_DIR, 'reset-pwd-code.txt')


@com(AppConf, AuthConf, AccService, OAuthService, SmtpService)
@route.path('acc')
class AccountCtl(Controller):
    def __init__(self, app_conf, auth_conf, acc_sv, oauth_sv, smtp_sv):
        self._app_conf = app_conf
        self._auth_conf = auth_conf
        self._acc_sv = acc_sv
        self._oauth_sv = oauth_sv
        self._smtp_sv = smtp_sv

    @route.get('me')
    def get_me(self, req, res):
        acc_id = self._oauth_sv.authen_req(req)
        acc = self._acc_sv.find_id(acc_id)
        if acc is None:
            raise Http500Error(req, 'Account identity not found')

        res.body = {
            '_id': str(acc['_id']),
            'name': acc['name'],
            'email': acc['email'],
            'phone': acc['phone'],
            'created_date': int(acc['created_date'].timestamp()),
            'modifired_date': int(acc['modified_date'].timestamp()),
            'last_action': acc['last_action']
        }

    @route.post('reg/code')
    def create_reg_code(self, req, res):
        info = req.body

        reg_code = self._acc_sv.mk_creation(
            info['name'], info['pwd'], info['email']
        )

        datetime_now = datetime.utcnow()
        expired_date = datetime_now + timedelta(self._acc_sv.create_time)
        values = {
            'REG_CODE': reg_code,
            'APP_NAME': self._app_conf.name,
            'SENDER_NAME': 'root',
            'SENDER_EMAIL': self._auth_conf.root_email,
            'REMOTE_ADDR': req.remote_addr,
            'ACC_NAME': info['name'],
            'EMAIL': info['email'],
            'DATETIME_NOW': datetime_now.strftime('%Y-%m-%d %H:%M:%S'),
            'EXPIRED_DATE': expired_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        txt_body = build_tpl(_REG_CODE_TMP_FILE, values)
        subject = 'Registration'
        self._smtp_sv.send(info['email'], subject, txt_body)

        res.status = 204

    @route.post('reg')
    def confirm_reg_code(self, req, res):
        reg_code = req.body['code']

        acc = self._acc_sv.confirm_creation(reg_code)

        datetime_now = datetime.utcnow()
        values = {
            'APP_NAME': self._app_conf.name,
            'SENDER_NAME': 'root',
            'SENDER_EMAIL': self._auth_conf.root_email,
            'REMOTE_ADDR': req.remote_addr,
            'ACC_NAME': acc['name'],
            'ACC_EMAIL': acc['email'],
            'DATETIME_NOW': datetime_now.strftime('%Y-%m-%d %H:%M:%S')
        }
        txt_body = build_tpl(_REG_TMP_FILE, values)
        subject = 'Registration'
        self._smtp_sv.send(acc['email'], subject, txt_body)

        res.status = 204

    @route.put('me/pwd')
    def change_pwd(self, req, res):
        new_pwd = req.body['new_pwd']

        acc_id = self._oauth_sv.authen_req(req)
        acc = self._acc_sv.find_id(acc_id)
        if acc is None:
            raise Http500Error(req, 'Account identity not found')
        self._acc_sv.change_pwd(acc_id, new_pwd)

        datetime_now = datetime.utcnow()
        values = {
            'APP_NAME': self._app_conf.name,
            'SENDER_NAME': 'root',
            'SENDER_EMAIL': self._auth_conf.root_email,
            'REMOTE_ADDR': req.remote_addr,
            'ACC_NAME': acc['name'],
            'DATETIME_NOW': datetime_now.strftime('%Y-%m-%d %H:%M:%S')
        }
        txt_body = build_tpl(_CHANGE_PWD_TMP_FILE, values)
        subject = 'Change password'
        self._smtp_sv.send(acc['email'], subject, txt_body)

        res.status = 204

    @route.post('pwd/code')
    def create_reset_pwd_code(self, req, res):
        email = req.body['email']

        acc = self._acc_sv.find_email(email)
        if acc is None:
            raise Http404Error(req, 'Email does not exist')

        reset_code = self._acc_sv.reset_pwd_code(email)
        expired_date = datetime.utcnow() + timedelta(hours=1)

        values = {
            'RESET_PWD_CODE': reset_code,
            'APP_NAME': self._app_conf.name,
            'SENDER_NAME': 'root',
            'SENDER_EMAIL': self._auth_conf.root_email,
            'REMOTE_ADDR': req.remote_addr,
            'DATETIME_NOW': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'EXPIRED_DATE': expired_date.strftime('%Y-%m-%d %H:%M:%S'),
            'ACC_NAME': acc['name']
        }
        txt_body = build_tpl(_RESET_PWD_CODE_TMP_FILE, values)

        subject = 'Reset password code'
        self._smtp_sv.send(email, subject, txt_body)

        res.status = 204

    @route.post('pwd')
    def confirm_reset_pwd_code(self, req, res):
        reset_code = req.body['code']
        new_pwd = req.body['new_pwd']

        acc_id = self._acc_sv.reset_pwd(reset_code, new_pwd)

        acc = self._acc_sv.find_id(acc_id)
        if acc is None:
            raise Http500Error(req)

        values = {
            'NEW_PWD': new_pwd,
            'RESET_PWD_CODE': reset_code,
            'ACC_NAME': acc['name'],
            'APP_NAME': self._app_conf.name,
            'REMOTE_ADDR': req.remote_addr,
            'DATETIME_NOW': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'SENDER_NAME': 'root',
            'SENDER_EMAIL': self._auth_conf.root_email,
        }
        txt_msg = build_tpl(_RESET_PWD_TMP_FILE, values)

        subject = 'Reset password'
        self._smtp_sv.send(acc['email'], subject, txt_msg)

        res.status = 204
