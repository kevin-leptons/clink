from clink.auth import AccMgr, OAuth


def test_get_accmgr(auth):
    assert type(auth.accmgr) is AccMgr


def test_get_auth(auth):
    assert type(auth.auth) is OAuth
