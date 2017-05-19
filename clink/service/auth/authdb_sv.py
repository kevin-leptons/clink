from pymongo import ASCENDING, IndexModel

from clink.service.mongo import MongoDocSpec

from clink.com import com
from clink.type.com import Service
from clink.service.mongo import MongoService

_ROOT_NAME = 'root'
_ACC_DOCNAME = 'account'
_GRP_DOCNAME = 'group'
_RPWD_DOCNAME = 'rpwd'
_ACCTMP_DOCNAME = 'acctmp'

_ACC_IND_1 = IndexModel([('name', ASCENDING)], unique=True)
_ACC_IND_2 = IndexModel([('email', ASCENDING)], unique=True)
_ACC_DOCSPEC = MongoDocSpec(_ACC_DOCNAME, [_ACC_IND_1, _ACC_IND_2])

_GRP_IND_1 = IndexModel([('name', ASCENDING)], unique=True)
_GRP_DOCSPEC = MongoDocSpec(_GRP_DOCNAME, [_GRP_IND_1])

_RPWD_DOCSPEC = MongoDocSpec(_RPWD_DOCNAME, [])

_ACCTMP_DOCSPEC = MongoDocSpec(_ACCTMP_DOCNAME, _ACC_DOCSPEC.indexes)

_DOC_SPECS = [_ACC_DOCSPEC, _GRP_DOCSPEC, _RPWD_DOCSPEC, _ACCTMP_DOCSPEC]


@com(MongoService)
class AuthDbService(Service):
    def __init__(self, mongo_sv):
        mongo_sv.use_docspecs(_DOC_SPECS)
