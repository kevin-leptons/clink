'''
SYNOPSIS

    POST /acc/reg/code
    POST /acc/reg

    GET  /acc/me
    PUT  /acc/me/pwd
    POST /acc/me/pwd/code
    POST /acc/me/pwd

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

from ..routing import Route
from ..error.http import Http401Error, Http400Error, Http500Error
from .util import build_template


_DIR = realpath(dirname(__file__))
_REG_CODE_TMP_FILE = path.join(_DIR, 'reg-code-tmp.txt')
_REG_TMP_FILE = path.join(_DIR, 'reg-tmp.txt')
_CHANGE_PWD_TMP_FILE = path.join(_DIR, 'change-pwd-tmp.txt')
_RESET_PWD_TMP_FILE = path.join(_DIR, 'reset-pwd-tmp.txt')
_RESET_PWD_CODE_TMP_FILE = path.join(_DIR, 'reset-pwd-code-tmp.txt')

route = Route('acc')


@route.post('reg/code')
def create_reg_code(req, res, ctx):
    accmgr = ctx['auth'].accmgr
    mailsv = ctx['mailsv']
    info = req.body

    reg_code = accmgr.mk_creation(info['name'], info['pwd'], info['email'])

    datetime_now = datetime.utcnow()
    expired_date = datetime_now + timedelta(accmgr.create_time)
    values = {
        'REG_CODE': reg_code,
        'APP_NAME': ctx['name'],
        'SENDER_NAME': 'root',
        'SENDER_EMAIL': ctx['rootmail'],
        'REMOTE_ADDR': req.remote_addr,
        'ACC_NAME': info['name'],
        'EMAIL': info['email'],
        'DATETIME_NOW': datetime_now.strftime('%Y-%m-%d %H:%M:%S'),
        'EXPIRED_DATE': expired_date.strftime('%Y-%m-%d %H:%M:%S')
    }
    txt_body = build_template(_REG_CODE_TMP_FILE, values)
    subject = 'Registration'
    mailsv.send(info['email'], subject, txt_body)

    res.status = 204


@route.post('reg')
def confirm_reg_code(req, res, ctx):
    accmgr = ctx['auth'].accmgr
    mailsv = ctx['mailsv']
    reg_code = req.body['code']

    acc = accmgr.confirm_creation(reg_code)

    datetime_now = datetime.utcnow()
    values = {
        'APP_NAME': ctx['name'],
        'SENDER_NAME': 'root',
        'SENDER_EMAIL': ctx['rootmail'],
        'REMOTE_ADDR': req.remote_addr,
        'ACC_NAME': acc['name'],
        'ACC_EMAIL': acc['email'],
        'DATETIME_NOW': datetime_now.strftime('%Y-%m-%d %H:%M:%S')
    }
    txt_body = build_template(_REG_TMP_FILE, values)
    subject = 'Registration'
    mailsv.send(acc['email'], subject, txt_body)

    res.status = 204


@route.put('me/pwd')
def change_pwd(req, res, ctx):
    auth = ctx['auth'].auth
    accmgr = ctx['auth'].accmgr
    mailsv = ctx['mailsv']
    new_pwd = req.body['new_pwd']

    acc_id = _authen(req, ctx)
    accmgr.change_pwd(acc_id, new_pwd)

    acc = accmgr.find_id(acc_id)
    if acc is None:
        raise Http500Error(req, 'Account identity not found')

    datetime_now = datetime.utcnow()
    values = {
        'APP_NAME': ctx['name'],
        'SENDER_NAME': 'root',
        'SENDER_EMAIL': ctx['rootmail'],
        'REMOTE_ADDR': req.remote_addr,
        'ACC_NAME': acc['name'],
        'DATETIME_NOW': datetime_now.strftime('%Y-%m-%d %H:%M:%S')
    }
    txt_body = build_template(_CHANGE_PWD_TMP_FILE, values)
    subject = 'Change password'
    mailsv.send(acc['email'], subject, txt_body)

    res.status = 204


@route.post('me/pwd/code')
def create_reset_pwd_code(req, res, ctx):
    accmgr = ctx['auth'].accmgr
    mailsv = ctx['mailsv']
    email = req.body['email']

    acc = accmgr.find_email(email)
    if acc is None:
        raise Http404Error(req, 'Email does not exist')

    reset_code = accmgr.reset_pwd_code(email)
    expired_date = datetime.utcnow() + timedelta(hours=1)

    values = {
        'RESET_PWD_CODE': reset_code,
        'APP_NAME': ctx['name'],
        'SENDER_NAME': 'root',
        'SENDER_EMAIL': ctx['rootmail'],
        'REMOTE_ADDR': req.remote_addr,
        'DATETIME_NOW': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        'EXPIRED_DATE': expired_date.strftime('%Y-%m-%d %H:%M:%S'),
        'ACC_NAME': acc['name']
    }
    txt_body = build_template(_RESET_PWD_CODE_TMP_FILE, values)

    subject = 'Reset password code'
    mailsv.send(email, subject, txt_body)

    res.status = 204


@route.post('me/pwd')
def confirm_reset_pwd_code(req, res, ctx):
    accmgr = ctx['auth'].accmgr
    mailsv = ctx['mailsv']
    reset_code = req.body['code']
    new_pwd = req.body['new_pwd']

    acc_id = accmgr.reset_pwd(reset_code, new_pwd)

    acc = accmgr.find_id(acc_id)
    if acc is None:
        raise Http500Error(req)

    values = {
        'NEW_PWD': new_pwd,
        'RESET_PWD_CODE': reset_code,
        'ACC_NAME': acc['name'],
        'APP_NAME': ctx['name'],
        'REMOTE_ADDR': req.remote_addr,
        'DATETIME_NOW': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        'SENDER_NAME': 'root',
        'SENDER_EMAIL': ctx['rootmail']
    }
    txt_msg = build_template(_RESET_PWD_TMP_FILE, values)

    subject = 'Reset password'
    mailsv.send(acc['email'], subject, txt_msg)

    res.status = 204


@route.get('me')
def get_me(req, res, ctx):
    auth = ctx['auth'].auth
    accmgr = ctx['auth'].accmgr
    acc_id = _authen(req, ctx)

    acc = accmgr.find_id(acc_id)
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


def _authen(req, ctx):
    # authorization header in format 'Bearer <token>'
    if 'AUTHORIZATION' not in req.header:
        raise Http401Error(req)
    auth_header = req.header['AUTHORIZATION']
    auth_type = auth_header[:7]
    if auth_type != 'Bearer ':
        raise Http400Error(req)
    atoken = auth_header[7:]

    return ctx['auth'].auth.authen(atoken)
