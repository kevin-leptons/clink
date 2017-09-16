from clink import stamp, mapper, Controller
from clink.service import OAuthSv, AccSv, SmtpSv, TemplateSv
from clink.error.http import Http406Error, Http400Error, Http401Error
from clink.util import fs


@stamp(OAuthSv, AccSv, SmtpSv, TemplateSv)
@mapper.path('/auth')
class AuthCtl(Controller):
    def __init__(self, oauth_sv, acc_sv, smtp_sv, tpl_sv):
        self._oauth_sv = oauth_sv
        self._acc_sv = acc_sv
        self._smtp_sv = smtp_sv
        self._tpl_sv = tpl_sv

        self._init_tpl_files()

    @mapper.post('/token')
    def get_token(self, req, res):
        info = req.body
        if info is None or 'grant_type' not in info:
            raise Http400Error(req, 'Require grant_type')
        grant_type = info['grant_type']

        if grant_type == 'password':
            if 'username' not in info:
                raise Http400Error(req, 'Require username')
            if 'password' not in info:
                raise Http400Error(req, 'Require password')

            acc = self._acc_sv.find_pwd(info['username'], info['password'])
            if acc is None:
                raise Http401Error(req, 'Name or password is invalid')
            res.body = self._oauth_sv.mktoken_pwd(
                info['username'], info['password']
            )
            values = {
                'acc_name': acc['name'],
                'remote_addr': req.remote_addr
            }
            txt_body = self._tpl_sv.build_file(self._LOGIN_TPL, values)

            subject = 'New login'
            self._smtp_sv.send(acc['email'], subject, txt_body)
        elif grant_type == 'refresh_token':
            if 'refresh_token' not in info:
                raise Http400Error(req, 'Require refresh_token')
            res.body = self._oauth_sv.mktoken_rtoken(info['refresh_token'])
        else:
            raise Http406Error(req, 'Not support grant_type=%s' % grant_type)

    def _init_tpl_files(self):
        '''
        Detect template files
        '''

        self._LOGIN_TPL = fs.asset_path('tpl/login.txt')
