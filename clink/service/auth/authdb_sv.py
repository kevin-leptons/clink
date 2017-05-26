from pymongo import ASCENDING, IndexModel

from clink.service.mongo import MongoDocSpec

from clink.com import stamp
from clink.type.com import Service
from clink.service.mongo import MongoSv

ROOT_NAME = 'root'
ACC_DOCNAME = 'account'
GRP_DOCNAME = 'group'
RPWD_DOCNAME = 'rpwd'
ACCTMP_DOCNAME = 'acctmp'
DOC_NAMES = [ACC_DOCNAME, GRP_DOCNAME, RPWD_DOCNAME, ACCTMP_DOCNAME]

_ACC_IND_1 = IndexModel([('name', ASCENDING)], unique=True)
_ACC_IND_2 = IndexModel([('email', ASCENDING)], unique=True)
_ACC_DOCSPEC = MongoDocSpec(ACC_DOCNAME, [_ACC_IND_1, _ACC_IND_2])

_GRP_IND_1 = IndexModel([('name', ASCENDING)], unique=True)
_GRP_DOCSPEC = MongoDocSpec(GRP_DOCNAME, [_GRP_IND_1])

_RPWD_DOCSPEC = MongoDocSpec(RPWD_DOCNAME, [])

_ACCTMP_DOCSPEC = MongoDocSpec(ACCTMP_DOCNAME, _ACC_DOCSPEC.indexes)

_DOC_SPECS = [_ACC_DOCSPEC, _GRP_DOCSPEC, _RPWD_DOCSPEC, _ACCTMP_DOCSPEC]


@stamp(MongoSv)
class AuthDbSv(Service):
    '''
    Ensure that database is compative with both AccSv and OAuthSv
    '''

    def __init__(self, mongo_sv):
        '''
        :param MongoSv mongo_sv:
        '''

        mongo_sv.use_docspecs(_DOC_SPECS)
        self._mongo_sv = mongo_sv

    def acc_doc(self):
        '''
        Return account collection

        :rtype: pymongo.collection.Collection
        '''

        return self._mongo_sv.doc(ACC_DOCNAME)

    def grp_doc(self):
        '''
        Return group collection

        :rtype: pymongo.collection.Collection
        '''

        return self._mongo_sv.doc(GRP_DOCNAME)

    def rpwd_doc(self):
        '''
        Return refresh token collection

        :rtype: pymongo.collection.Collection
        '''

        return self._mongo_sv.doc(RPWD_DOCNAME)

    def acctmp_doc(self):
        '''
        Return temporary account collection

        :rtype: pymongo.collection.Collection
        '''

        return self._mongo_sv.doc(ACCTMP_DOCNAME)
