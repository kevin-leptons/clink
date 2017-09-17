from clink.error.http import Http404Error, Http400Error, Http403Error
from clink import stamp, mapper, AppConf, AuthConf, Controller
from clink.service import AccSv, TemplateSv, SmtpSv, OAuthSv
from clink.util import fs


@stamp(AppConf, AuthConf, AccSv, OAuthSv, SmtpSv, TemplateSv)
@mapper.path('/acc')
class AccCtl(Controller):
    '''
    Manage accounts and related concepts
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

        self._init_tpl_files()

    @mapper.post('/reg/code')
    def mk_reg_code(self, req, res):
        if req.body is None:
            raise Http400Error(req, 'Require name, pwd, email')
        if 'name' not in req.body:
            raise Http400Error(req, 'Require name')
        if 'pwd' not in req.body:
            raise Http400Error(req, 'Require pwd')
        if 'email' not in req.body:
            raise Http400Error(req, 'Require email')

        result = self._acc_sv.mk_reg_code(
            req.body['name'], req.body['pwd'], req.body['email']
        )

        values = {
            'reg_code': result.code,
            'acc_name': req.body['name'],
            'acc_email': req.body['email'],
            'expired_date': result.exp_date.strftime('%Y-%m-%d %H:%M:%S'),
            'remote_addr': req.remote_addr
        }
        txt_body = self._tpl_sv.build_file(self._REG_CODE_TPL, values)
        subject = 'Registration'
        self._smtp_sv.send(req.body['email'], subject, txt_body)

        res.status = 204

    @mapper.post('/reg')
    def confirm_reg_code(self, req, res):
        if req.body is None or 'code' not in req.body:
            raise Http400Error(req, 'Require code')
        reg_code = req.body['code']

        acc = self._acc_sv.cf_reg_code(reg_code)

        values = {
            'acc_name': acc['name'],
            'acc_email': acc['email'],
            'remote_addr': req.remote_addr
        }
        txt_body = self._tpl_sv.build_file(self._REG_TPL, values)
        subject = 'Registration'
        self._smtp_sv.send(acc['email'], subject, txt_body)

        res.status = 204

    @mapper.get('/me')
    def acc_info(self, req, res):
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
            'modified_date': int(acc['modified_date'].timestamp()),
            'last_action': acc['last_action']
        }

    @mapper.put('/me/pwd')
    def change_pwd(self, req, res):
        if req.body is None:
            raise Http400Error(req, 'Require old_pwd, new_pwd')
        if 'old_pwd' not in req.body:
            raise Http400Error(req, 'Require old_pwd')
        if 'new_pwd' not in req.body:
            raise Http400Error(req, 'Require new_pwd')
        old_pwd = req.body['old_pwd']
        new_pwd = req.body['new_pwd']

        acc_id = self._oauth_sv.authen_req(req)
        acc = self._acc_sv.find_id(acc_id)
        if acc is None:
            raise Http404Error(req, 'Not found identity %s' % str(acc_id))
        acc = self._acc_sv.find_pwd(acc['name'], old_pwd)
        if acc is None:
            raise Http403Error(req, 'Old password is invalid')

        self._acc_sv.ch_pwd(acc_id, new_pwd)

        values = {
            'acc_name': acc['name'],
            'remote_addr': req.remote_addr
        }
        txt_body = self._tpl_sv.build_file(self._CHPWD_TPL, values)
        subject = 'Change password'
        self._smtp_sv.send(acc['email'], subject, txt_body)

        res.status = 204

    @mapper.post('/pwd/code')
    def mk_reset_pwd_code(self, req, res):
        if req.body is None or 'email' not in req.body:
            raise Http400Error(req, 'Require email')
        email = req.body['email']

        acc = self._acc_sv.find_email(email)
        if acc is None:
            raise Http400Error(req, 'Email does not exist')

        result = self._acc_sv.mk_rpwd_code(email)

        values = {
            'reset_pwd_code': result.code,
            'app_name': self._app_conf.name,
            'acc_name': acc['name'],
            'expired_date': result.exp_date.strftime('%Y-%m-%d %H:%M:%S'),
            'remote_addr': req.remote_addr
        }

        txt_body = self._tpl_sv.build_file(self._RPWD_CODE_TPL, values)
        subject = 'Reset password code'
        self._smtp_sv.send(email, subject, txt_body)

        res.status = 204

    @mapper.post('/pwd')
    def confirm_reset_pwd_code(self, req, res):
        if req.body is None:
            raise Http400Error(req, 'Require code, new_pwd')
        if 'code' not in req.body:
            raise Http400Error(req, 'Require code')
        if 'new_pwd' not in req.body:
            raise Http400Error(req, 'Require new_pwd')
        reset_code = req.body['code']
        new_pwd = req.body['new_pwd']

        acc_id = self._acc_sv.cf_rpwd_code(reset_code, new_pwd)

        acc = self._acc_sv.find_id(acc_id)
        if acc is None:
            raise Http404Error(req, 'Not found identity %s' % str(acc_id))

        values = {
            'acc_name': acc['name'],
            'remote_addr': req.remote_addr
        }

        txt_msg = self._tpl_sv.build_file(self._RPWD_TPL, values)
        subject = 'Reset password'
        self._smtp_sv.send(acc['email'], subject, txt_msg)

        res.status = 204

    def _init_tpl_files(self):
        '''
        Detect template files
        '''

        self._REG_CODE_TPL = fs.asset_path('tpl/reg-code.txt')
        self._REG_TPL = fs.asset_path('tpl/reg-tmp.txt')
        self._CHPWD_TPL = fs.asset_path('tpl/change-pwd.txt')
        self._RPWD_TPL = fs.asset_path('tpl/reset-pwd.txt')
        self._RPWD_CODE_TPL = fs.asset_path('tpl/reset-pwd-code.txt')
