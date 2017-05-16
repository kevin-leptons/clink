from os import path
from os.path import dirname, realpath
from datetime import datetime, timedelta
from bson import ObjectId

from ..routing import Route
from ..error.http import Http401Error, Http400Error, Http500Error
from .util import build_template


_DIR = realpath(dirname(__file__))
_RESET_PWD_TMP_FILE = path.join(_DIR, 'reset-pwd-tmp.txt')
_RESET_PWD_CODE_TMP_FILE = path.join(_DIR, 'reset-pwd-code-tmp.txt')

route = Route('account')


@route.post('')
def register(req, res, ctx):
    accmgr = ctx['auth'].accmgr
    info = req.body

    accmgr.create(info['name'], info['password'], info['email'])
    res.status = 204


@route.get('me')
def get_me(req, res, ctx):
    auth = ctx['auth'].auth
    accmgr = ctx['auth'].accmgr
    acc_id = _authen(req, ctx)

    acc = accmgr.find_id(acc_id)
    res.body = {
        '_id': str(acc['_id']),
        'name': acc['name'],
        'email': acc['email'],
        'phone': acc['phone'],
        'created_date': int(acc['created_date'].timestamp()),
        'modifired_date': int(acc['modified_date'].timestamp()),
        'last_action': acc['last_action']
    }


@route.put('me/pwd')
def put_password(req, res, ctx):
    auth = ctx['auth'].auth
    accmgr = ctx['auth'].accmgr

    acc_id = _authen(req, ctx)
    accmgr.change_pwd(acc_id, req.body['password'])
    res.status = 204


@route.get('me/pwd/code')
def get_reset_pwd_code(req, res, ctx):
    accmgr = ctx['auth'].accmgr
    mailsv = ctx['mailsv']
    email = req.args['email']

    acc = accmgr.find_email(email)
    if acc is None:
        raise Http404Error(req, 'Email does not exist')

    reset_code = accmgr.reset_pwd_code(email)
    expired_date = datetime.utcnow() + timedelta(hours=1)

    f = open(_RESET_PWD_CODE_TMP_FILE)
    txt_body = f.read()
    f.close()
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
    txt_body = build_template(txt_body, values)

    subject = 'Reset password code'
    mailsv.send(email, subject, txt_body)

    res.status = 204


@route.post('me/pwd')
def post_password(req, res, ctx):
    accmgr = ctx['auth'].accmgr
    mailsv = ctx['mailsv']
    reset_code = req.body['code']
    new_pwd = req.body['new_pwd']

    acc_id = accmgr.reset_pwd(reset_code, new_pwd)

    acc = accmgr.find_id(acc_id)
    if acc is None:
        raise Http500Error(req)

    f = open(_RESET_PWD_TMP_FILE)
    txt_msg = f.read()
    f.close()
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
    txt_msg = build_template(txt_msg, values)

    subject = 'Reset password'
    mailsv.send(acc['email'], subject, txt_msg)

    res.status = 204


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
