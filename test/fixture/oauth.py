from pytest import fixture


@fixture(scope='module')
def oauth(auth):
    return auth.auth


@fixture
def exist_token(oauth, exist_acc):
    username = exist_acc['username']
    password = exist_acc['password']

    return oauth.mktoken_pwd(username, password)
