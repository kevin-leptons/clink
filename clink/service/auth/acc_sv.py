import random
from datetime import datetime, timedelta
from time import time
from string import ascii_lowercase, ascii_uppercase, digits
from hashlib import sha224

from clink.type import Service, AuthConf
from clink.com import stamp
from clink.dflow import verify, ExistError, NonExistError, ExpiredError
from clink.model.std import acc_name as name_model, acc_pwd as pwd_model
from clink.model.std import email as email_model, phone as phone_model
from clink.model.acc import confirm_code as confirm_code_model

from .authdb_sv import AuthDbSv
from .type import ConfirmCodeSpec

_ACT_REGISTERED = 'REGISTERED'
_ACT_CHANGE_PWD = 'CHANGE_PWD'
_ACT_RESET_PWD = 'RESET_PWD'
_ACT_ADD_TO_GRP = 'ADD_TO_GRP'
_ACT_RM_FRM_GRP = 'RM_FRM_GRP'

_PWD_CHARS = ascii_lowercase + ascii_uppercase + digits
_CODE_CHARS = ascii_uppercase


def _hash_pwd(password):
    return sha224(password.encode('utf-8')).hexdigest()


def _rand_pwd():
    return ''.join(random.sample(_PWD_CHARS, 6))


def rand_code():
    a = ''.join(random.sample(_CODE_CHARS, 4))
    b = ''.join(random.sample(_CODE_CHARS, 4))
    c = ''.join(random.sample(_CODE_CHARS, 4))
    d = ''.join(random.sample(_CODE_CHARS, 4))

    return '-'.join([a, b, c, d])


@stamp(AuthDbSv, AuthConf)
class AccSv(Service):
    '''
    Manage accounts and related concepts
    '''

    def __init__(self, authdb_sv, auth_conf):
        '''
        :param AuthDbSv authdb_sv:
        :param AuthConf auth_conf:
        '''

        self._acc_doc = authdb_sv.acc_doc()
        self._grp_doc = authdb_sv.grp_doc()
        self._rpwd_doc = authdb_sv.rpwd_doc()
        self._acctmp_doc = authdb_sv.acctmp_doc()

        self.rpwd_time = 3600
        self.create_time = 3600

        root_acc = self.find_name('root')
        if root_acc is None:
            self.mk_acc('root', auth_conf.root_pwd, auth_conf.root_email)

    @verify(None, name_model, pwd_model, email_model, phone_model)
    def mk_acc(self, name, password, email, phone=None):
        '''
        Create new account

        :param str name:
        :param str password:
        :param str email:
        :param str phone:
        :rtype: bson.objectid.ObjectId
        :raise TypeError:
        '''

        account = {
            'name': name,
            'hashpwd': _hash_pwd(password),
            'email': email,
            'phone': phone,
            'groups': [],
            'created_date': datetime.utcnow(),
            'modified_date': datetime.utcnow(),
            'last_action': _ACT_REGISTERED
        }
        result = self._acc_doc.insert_one(account)
        return result.inserted_id

    @verify(None, name_model, pwd_model, email_model, phone_model)
    def mk_reg_code(self, name, password, email, phone=None):
        '''
        Create a registration code. Use returned code with cf_reg_code()
        to create account

        :param str name:
        :param str password:
        :param str email:
        :param str phone:
        :rtype: ConfirmCodeSpec
        :raise TypeError:
        :raise ExistError:
        '''

        if self._acc_doc.find_one({'name': name}) is not None:
            raise ExistError({'name': name})
        if self._acc_doc.find_one({'email': email}) is not None:
            raise ExistError({'email': email})
        if phone is not None:
            if self._acc_doc.find_one({'phone': phone}) is not None:
                raise ExistError({'phone': phone})

        if self._acctmp_doc.find_one({'name': name}) is not None:
            raise ExistError({'name': name})
        if self._acctmp_doc.find_one({'email': email}) is not None:
            raise ExistError({'email': email})
        if phone is not None:
            if self._acctmp_doc.find_one({'phone': phone}) is not None:
                raise ExistError({'phone': 'phone'})

        datetime_now = datetime.utcnow().timestamp()
        self._acctmp_doc.delete_many({'_expired_date': {'$lt': datetime_now}})

        creation_code = rand_code()
        expired_date = datetime.utcnow() + timedelta(hours=self.create_time)
        acctmp = {
            'name': name,
            'hashpwd': _hash_pwd(password),
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

        return ConfirmCodeSpec(creation_code, expired_date)

    @verify(None, confirm_code_model)
    def cf_reg_code(self, code):
        '''
        Use registration code to create account

        :param str code:
        :rtype: dict
        :raise ExistError:
        :raise ExpiredError:
        '''

        acctmp = self._acctmp_doc.find_one({'_creation_code': code})
        if acctmp is None:
            raise NonExistError({'code': code})
        if acctmp['_expired_date'] < datetime.utcnow().timestamp():
            raise ExpiredError({'code': time()})
        self._acctmp_doc.delete_one({'_creation_code': code})

        del acctmp['_id']
        del acctmp['_expired_date']
        del acctmp['_creation_code']

        self._acc_doc.insert_one(acctmp)
        del acctmp['hashpwd']

        return acctmp

    def find_id(self, id):
        '''
        Find account by identity

        :param bson.objectid.ObjectId id:
        :rtype: dict
        '''

        return self._acc_doc.find_one({'_id': id})

    @verify(None, name_model)
    def find_name(self, name):
        '''
        Find account by name

        :param str name:
        :rtype: dict
        :raise TypeError:
        '''

        return self._acc_doc.find_one({'name': name})

    @verify(None, email_model)
    def find_email(self, email):
        '''
        Find account by email

        :param str email:
        :rtype: dict
        :raise TypeError:
        '''

        return self._acc_doc.find_one({'email': email})

    @verify(None, phone_model)
    def find_phone(self, phone):
        '''
        Find account by phone number

        :param str phone:
        :rtype: dict
        :raise TypeError:
        '''

        return self._acc_doc.find_one({'phone': phone})

    @verify(None, name_model, pwd_model)
    def find_pwd(self, name, pwd):
        '''
        Find account by name and password

        :param str name:
        :param str pwd:
        :rtype: dict
        :raise TypeError:
        '''

        hashpwd = _hash_pwd(pwd)
        return self._acc_doc.find_one({'name': name, 'hashpwd': hashpwd})

    def rm_acc(self, id):
        '''
        Remove account by identity

        :param bson.objectid.ObjectId id:
        '''

        result = self._acc_doc.delete_one({'_id': id})
        if result.deleted_count != 1:
            raise NonExistError({'id': id})

    @verify(None, None, pwd_model)
    def ch_pwd(self, id, new_pwd):
        '''
        Change password of account by identity

        :param bson.objectid.ObjectId id:
        :param str new_pwd:
        :raise TypeError:
        '''

        upd = {
            '$set': {
                'hashpwd': _hash_pwd(new_pwd),
                'modified_date': datetime.utcnow(),
                'last_action': _ACT_CHANGE_PWD
            }
        }
        result = self._acc_doc.update_one({'_id': id}, upd)

        if result.modified_count != 1:
            raise NonExistError({'id': id})

    @verify(None, email_model)
    def mk_rpwd_code(self, email):
        '''
        Create reset password code from email.
        Use returned code with cf_rpwd_code() to reset to new password

        :param str email:
        :rtype: ConfirmCodeSpec
        :raise TypeError:
        '''

        acc = self._acc_doc.find_one({'email': email})
        if acc is None:
            raise NonExistError({'email': email})
        self._rpwd_doc.delete_many({'acc_id': acc['_id']})

        reset_code = rand_code()
        exp_date = datetime.utcnow() + timedelta(hours=self.rpwd_time)
        code_spec = {
            'code': reset_code,
            'expired_date': exp_date.timestamp(),
            'acc_id': acc['_id'],
            'acc_email': acc['email']
        }
        self._rpwd_doc.insert_one(code_spec)

        return ConfirmCodeSpec(reset_code, exp_date)

    @verify(None, confirm_code_model, pwd_model)
    def cf_rpwd_code(self, code, new_pwd):
        '''
        Reset password from code

        :param str code:
        :param str new_pwd:
        :rtype: bson.objectid.ObjectId
        :raise TypeError:
        '''

        code_spec = self._rpwd_doc.find_one({'code': code})
        if code_spec is None:
            raise NonExistError({'code': code})
        if code_spec['expired_date'] < time():
            raise ExpiredError({'code': time()})

        acc_id = code_spec['acc_id']
        self._rpwd_doc.delete_many({'acc_id': acc_id})

        new_hashpwd = _hash_pwd(new_pwd)
        upd = {
            '$set': {
                'hashpwd': new_hashpwd,
                'last_action': _ACT_RESET_PWD
            }
        }
        self._acc_doc.update_one({'_id': acc_id}, upd)

        return acc_id

    def mk_group(self, group_name):
        '''
        Create new account group

        :param str group_name:
        '''

        self._grp_doc.insert_one({'name': group_name})

    def rm_group(self, group_name):
        '''
        Remove account group

        :param str group_name:
        '''

        result = self._grp_doc.delete_one({'name': group_name})

        if result.deleted_count != 1:
            raise NonExistError({'group_name': group_name})

    def add_to_group(self, acc_id, group_name):
        '''
        Put an account into group

        :param bson.objectid.ObjectId acc_id:
        :param str group_name:
        '''

        acc = self._acc_doc.find_one({'_id': acc_id})
        if acc is None:
            raise NonExistError({'id': acc_id})

        grp = self._grp_doc.find_one({'name': group_name})
        if grp is None:
            raise NonExistError({'group_name': group_name})
        if group_name in acc['groups']:
            raise ExistError({'group_name': group_name})

        upd = {
            '$push': {'groups': group_name},
            '$set': {'last_action': _ACT_ADD_TO_GRP}
        }
        self._acc_doc.update_one({'_id': acc_id}, upd)

    def del_fm_group(self, acc_id, group_name):
        '''
        Remove an account from group

        :param bson.objectid.ObjectId acc_id:
        :param str group_name:
        '''

        acc = self._acc_doc.find_one({'_id': acc_id})

        if acc is None:
            raise NonExistError({'id': acc_id})
        if group_name not in acc['groups']:
            raise NonExistError({'group_name': group_name})

        upd = {
            '$pull': {'groups': group_name},
            '$set': {'last_action': _ACT_RM_FRM_GRP}
        }
        self._acc_doc.update_one({'_id': acc_id}, upd)
