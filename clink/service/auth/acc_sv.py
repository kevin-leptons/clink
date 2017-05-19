'''
SYNOPSIS

    class AccMgr(acc_doc, grp_doc)
        create(self, name, password, email, phone=None)
        find_id(self, id)
        find_name(self, name)
        remove(self, id)
        change_pwd(self, id, new_pwd)
        reset_pwd(self, email)
        add_group(self, group_name)
        del_group(self, group_name)
        add_to_group(self, acc_id, group_name)
        del_fm_group(self, acc_id, group_name)

DESCRIPTION

    Manage accounts and groups.
'''

from datetime import datetime, timedelta
from time import time
from string import ascii_lowercase, ascii_uppercase, digits

from clink.type.com import Service
from clink.com import com
from clink.service.mongo import MongoService

from .error import AccountNotExist, GroupExist, GroupNotExist, \
                   CodeNotExistError, CodeExpiredError, AccountExistError, \
                   EmailExistError
from .authdb_sv import AuthDbService
from .type import AuthConf
from .util import hash_pwd, rand_pwd, rand_code

_ACT_REGISTERED = 'REGISTERED'
_ACT_CHANGE_PWD = 'CHANGE_PWD'
_ACT_RESET_PWD = 'RESET_PWD'
_ACT_ADD_TO_GRP = 'ADD_TO_GRP'
_ACT_RM_FRM_GRP = 'RM_FRM_GRP'


@com(MongoService, AuthDbService, AuthConf)
class AccService(Service):
    _pwd_chars = ascii_lowercase + ascii_uppercase + digits

    def __init__(self, mongo_sv, authdb_sv, auth_conf):
        pass
        self._acc_doc = mongo_sv.doc('account')
        self._grp_doc = mongo_sv.doc('group')
        self._rpwd_doc = mongo_sv.doc('rpwd')
        self._acctmp_doc = mongo_sv.doc('acctmp')

        self.rpwd_time = 3600
        self.create_time = 3600

        root_acc = self.find_name('root')
        if root_acc is None:
            self.create('root', auth_conf.root_pwd, auth_conf.root_email)

    def create(self, name, password, email, phone=None):
        account = {
            'name': name,
            'hashpwd': hash_pwd(password),
            'email': email,
            'phone': phone,
            'groups': [],
            'created_date': datetime.utcnow(),
            'modified_date': datetime.utcnow(),
            'last_action': _ACT_REGISTERED
        }
        result = self._acc_doc.insert_one(account)
        return result.inserted_id

    def mk_creation(self, name, password, email, phone=None):
        if self._acc_doc.find_one({'name': name}) is not None:
            raise AccountExistError(name)
        if self._acc_doc.find_one({'email': email}) is not None:
            raise EmailExistError(email)
        if phone is not None:
            if self._acc_doc.find_one({'phone': phone}) is not None:
                raise PhoneExistError(phone)

        datetime_now = datetime.utcnow().timestamp()
        self._acctmp_doc.delete_many({'_expired_date': {'$lt': datetime_now}})

        creation_code = rand_code()
        expired_date = datetime.utcnow() + timedelta(hours=self.create_time)
        acctmp = {
            'name': name,
            'hashpwd': hash_pwd(password),
            'email': email,
            'phone': phone,
            'groups': [],
            'created_date': datetime.utcnow(),
            'modified_date': datetime.utcnow(),
            'last_action': _ACT_REGISTERED,

            '_expired_date': expired_date.timestamp(),
            '_creation_code': creation_code
        }
        self._acctmp_doc.insert_one(acctmp)

        return creation_code

    def confirm_creation(self, code):
        acctmp = self._acctmp_doc.find_one({'_creation_code': code})
        if acctmp is None:
            raise CodeNotExistError(code)
        if acctmp['_expired_date'] < datetime.utcnow().timestamp():
            raise CodeExpiredError(code)
        self._acctmp_doc.delete_one({'_creation_code': code})

        del acctmp['_id']
        del acctmp['_expired_date']
        del acctmp['_creation_code']

        result = self._acc_doc.insert_one(acctmp)
        del acctmp['hashpwd']

        return acctmp

    def find_id(self, id):
        return self._acc_doc.find_one({'_id': id})

    def find_name(self, name):
        return self._acc_doc.find_one({'name': name})

    def find_email(self, email):
        return self._acc_doc.find_one({'email': email})

    def remove(self, id):
        result = self._acc_doc.delete_one({'_id': id})
        if result.deleted_count != 1:
            raise AccountNotExist(id)

    def change_pwd(self, id, new_pwd):
        upd = {
            '$set': {
                'hashpwd': hash_pwd(new_pwd),
                'modified_date': datetime.utcnow(),
                'last_action': _ACT_CHANGE_PWD
            }
        }
        result = self._acc_doc.update_one({'_id': id}, upd)

        if result.modified_count != 1:
            raise AccountNotExist(id)

    def reset_pwd_code(self, email):
        acc = self._acc_doc.find_one({'email': email})
        if acc is None:
            raise AccountNotExist(email)
        self._rpwd_doc.delete_many({'acc_id': acc['_id']})

        reset_code = rand_code()
        code_spec = {
            'code': reset_code,
            'expired_date': time() + self.rpwd_time,
            'acc_id': acc['_id'],
            'acc_email': acc['email']
        }
        self._rpwd_doc.insert_one(code_spec)

        return reset_code

    def reset_pwd(self, code, new_pwd):
        code_spec = self._rpwd_doc.find_one({'code': code})
        if code_spec is None:
            raise CodeNotExistError(code)
        if code_spec['expired_date'] < time():
            raise CodeExpiredError()

        acc_id = code_spec['acc_id']
        self._rpwd_doc.delete_many({'acc_id': acc_id})

        new_hashpwd = hash_pwd(new_pwd)
        upd = {
            '$set': {
                'hashpwd': new_hashpwd,
                'last_action': _ACT_RESET_PWD
            }
        }
        self._acc_doc.update_one({'_id': acc_id}, upd)

        return acc_id

    def add_group(self, group_name):
        self._grp_doc.insert_one({'name': group_name})

    def del_group(self, group_name):
        result = self._grp_doc.delete_one({'name': group_name})

        if result.deleted_count != 1:
            raise GroupNotExist(group_name)

    def add_to_group(self, acc_id, group_name):
        acc = self._acc_doc.find_one({'_id': acc_id})
        if acc is None:
            raise AccountNotExist(acc_id)

        grp = self._grp_doc.find_one({'name': group_name})
        if grp is None:
            raise GroupNotExist(group_name)
        if group_name in acc['groups']:
            raise GroupExist(group_name)

        upd = {
            '$push': {'groups': group_name},
            '$set': {'last_action': _ACT_ADD_TO_GRP}
        }
        self._acc_doc.update_one({'_id': acc_id}, upd)

    def del_fm_group(self, acc_id, group_name):
        acc = self._acc_doc.find_one({'_id': acc_id})

        if acc is None:
            raise AccountNotExist(acc_id)
        if group_name not in acc['groups']:
            raise GroupNotExist(group_name)

        upd = {
            '$pull': {'groups': group_name},
            '$set': {'last_action': _ACT_RM_FRM_GRP}
        }
        self._acc_doc.update_one({'_id': acc_id}, upd)
