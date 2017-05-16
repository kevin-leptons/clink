from pytest import raises
from pymongo.errors import DuplicateKeyError
from bson import ObjectId

from clink.auth.error import AccountNotExist, GroupNotExist


def test_create(accmgr, rand):
    username = rand.username()
    email = rand.email()
    password = rand.password()

    id = accmgr.create(username, password, email)
    assert id is not None


def test_create_dup_username(accmgr, rand, exist_acc):
    with raises(DuplicateKeyError):
        accmgr.create(exist_acc['username'], rand.password(), rand.email())


def test_create_dup_email(accmgr, rand, exist_acc):
    with raises(DuplicateKeyError):
        accmgr.create(rand.username(), rand.password(), exist_acc['email'])


def test_find_id(accmgr, exist_acc):
    acc = accmgr.find_id(exist_acc['_id'])

    assert acc is not None


def test_find_id_not_found(accmgr):
    id = ObjectId()
    acc = accmgr.find_id(id)

    assert acc is None


def test_find_usr(accmgr, exist_acc):
    acc = accmgr.find_usr(exist_acc['username'])
    assert acc is not None


def test_find_name_not_found(accmgr, rand):
    acc = accmgr.find_usr(rand.username())
    assert acc is None


def test_remove(accmgr, exist_acc):
    accmgr.remove(exist_acc['_id'])


def test_remove_not_found(accmgr, rand):
    id = ObjectId()

    with raises(AccountNotExist):
        accmgr.remove(id) is False


def test_change_pwd(accmgr, exist_acc, rand):
    id = exist_acc['_id']
    new_pwd = rand.password()

    accmgr.change_pwd(id, new_pwd)


def test_change_pwd_not_found(accmgr, rand):
    id = ObjectId()
    new_pwd = rand.password()

    with raises(AccountNotExist):
        accmgr.change_pwd(id, new_pwd)


def test_reset_pwd(accmgr, rand, exist_acc):
    email = exist_acc['email']

    new_pwd = accmgr.reset_pwd(email)

    assert new_pwd is not None


def test_reset_pwd_not_found(accmgr, rand):
    email = rand.email()

    with raises(AccountNotExist):
        accmgr.reset_pwd(email)


def test_add_group(accmgr, rand):
    accmgr.add_group(rand.group())


def test_del_group(accmgr, exist_grp):
    accmgr.del_group(exist_grp['name'])


def test_del_group_not_found(accmgr, rand):
    with raises(GroupNotExist):
        assert accmgr.del_group(rand.group())


def test_add_to_group(accmgr, exist_acc, exist_grp):
    accmgr.add_to_group(exist_acc['_id'], exist_grp['name'])


def test_add_to_group_not_found(accmgr, exist_acc, rand):
    acc_id = exist_acc['_id']
    grp_name = rand.group()

    with raises(GroupNotExist):
        accmgr.add_to_group(acc_id, grp_name)


def test_add_to_group_acc_not_found(accmgr, exist_grp, rand):
    acc_id = ObjectId()
    grp_name = exist_grp['name']

    with raises(AccountNotExist):
        accmgr.add_to_group(acc_id, grp_name)


def test_del_fm_group(accmgr, exist_acc, exist_grp):
    acc_id = exist_acc['_id']
    grp_name = exist_grp['name']

    accmgr.add_to_group(acc_id, grp_name)
    accmgr.del_fm_group(acc_id, grp_name)


def test_del_fm_group_not_found(accmgr, exist_acc, rand):
    acc_id = exist_acc['_id']
    grp_name = rand.group()

    with raises(GroupNotExist):
        accmgr.del_fm_group(acc_id, grp_name)


def test_del_fm_group_acc_not_found(accmgr, exist_grp):
    acc_id = ObjectId()
    grp_name = exist_grp['name']

    with raises(AccountNotExist):
        accmgr.del_fm_group(acc_id, grp_name)
