from pytest import fixture


@fixture(scope='module')
def accmgr(auth):
    return auth.accmgr


@fixture()
def exist_acc(accmgr, rand):
    username = rand.username()
    password = rand.password()
    email = rand.email()

    id = accmgr.create(username, password, email)
    return {
        '_id': id,
        'username': username,
        'password': password,
        'email': email
    }


@fixture()
def exist_grp(accmgr, rand):
    name = rand.group()

    id = accmgr.add_group(name)
    return {'_id': id, 'name': name}
