from pytest import raises
from jwt.exceptions import DecodeError
from clink.auth.error import PasswordError, AccountNotExist


def test_mktoken_pwd(oauth, exist_acc):
    username = exist_acc['username']
    password = exist_acc['password']

    token = oauth.mktoken_pwd(username, password)

    assert token is not None


def test_mktoken_pwd_usr_error(oauth, rand):
    username = rand.username()
    password = rand.password()

    with raises(AccountNotExist):
        oauth.mktoken_pwd(username, password)


def test_mktoken_pwd_error(oauth, exist_acc, rand):
    username = exist_acc['username']
    password = rand.password()

    with raises(PasswordError):
        oauth.mktoken_pwd(username, password)


def test_mktoken_rtoken(oauth, exist_token):
    rtoken = exist_token['refresh_token']
    new_token = oauth.mktoken_rtoken(rtoken)

    assert new_token is not None


def test_mktoken_rtoken_invalid(oauth, rand):
    rtoken = rand.string()

    with raises(DecodeError):
        oauth.mktoken_rtoken(rtoken)


def test_authen(oauth, exist_token):
    access_token = exist_token['access_token']
    acc_id = oauth.authen(access_token)

    assert acc_id is not None
