from pymongo import ASCENDING, IndexModel

from ..db import MongoDocSpec

from .iauth import IAuth
from .accmgr import AccMgr
from .oauth import OAuth

_ROOT_NAME = 'root'
_ACC_DOCNAME = 'account'
_GRP_DOCNAME = 'group'
_RPWD_DOCNAME = 'rpwd'

_ACC_IND_1 = IndexModel([('name', ASCENDING)], unique=True)
_ACC_IND_2 = IndexModel([('email', ASCENDING)], unique=True)
_ACC_DOCSPEC = MongoDocSpec(_ACC_DOCNAME, [_ACC_IND_1, _ACC_IND_2])

_GRP_IND_1 = IndexModel([('name', ASCENDING)], unique=True)
_GRP_DOCSPEC = MongoDocSpec(_GRP_DOCNAME, [_GRP_IND_1])

_RPWD_DOCSPEC = MongoDocSpec(_RPWD_DOCNAME, [])


class Auth(IAuth):
    def __init__(
        self, dbnode, root_pwd, root_email, jwt_key,
        token_time=4*3600, rtoken_time=30*24*3600
    ):
        dbnode.use_docspecs([_ACC_DOCSPEC, _GRP_DOCSPEC, _RPWD_DOCSPEC])

        acc_doc, grp_doc = dbnode.docs(_ACC_DOCNAME, _GRP_DOCNAME)
        rpwd_doc = dbnode.doc(_RPWD_DOCNAME)
        self._accmgr = AccMgr(acc_doc, grp_doc, rpwd_doc)
        self._auth = OAuth(acc_doc, grp_doc, jwt_key, token_time, rtoken_time)

        root_acc = self._accmgr.find_name(_ROOT_NAME)
        if root_acc is None:
            self._accmgr.create(_ROOT_NAME, root_pwd, root_email)

    @property
    def accmgr(self):
        return self._accmgr

    @property
    def auth(self):
        return self._auth
