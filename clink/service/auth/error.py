class PhoneExistError(Exception):
    def __init__(self, phone_numer):
        self._msg = phone_numer

    def __str__(self):
        return self._msg


class DocDeniedError(Exception):
    def __init__(self, doc_name):
        self._msg = 'You MUST NOT access outside auth scope: %s' % doc_name

    def __str__(self):
        return self._msg


class AccountExistError(Exception):
    def __init__(self, identity):
        self._msg = identity

    def __str__(self):
        return self._msg


class AccountNotExist(Exception):
    def __init__(self, identity):
        self._msg = identity

    def __str__(self):
        return self._msg


class GroupExist(Exception):
    def __init__(self, identity):
        self._msg = identity

    def __str__(self):
        return self._msg


class GroupNotExist(Exception):
    def __init__(self, identity):
        self._msg = identity

    def __str__(self):
        return self._msg


class PasswordError(Exception):
    def __init__(self, name, password):
        self._msg = 'usr=%s, pwd=%s' % (name, password)

    def __str__(self):
        return self._msg


class RTokenExpiredError(Exception):
    def __init__(self, rtoken_spec):
        self._msg = 'rtoken={}, created_date=[], expired_date={}'.format(
            rtoken_spec['value'], rtoken_spec['test_create'],
            rtoken_spec['expired_date']
        )

    def __str__(self):
        return self._msg


class TokenExpiredError(Exception):
    def __init__(self, atoken_raw):
        self._msg = 'sub=%s, exp=%s' % (atoken_raw['sub'], atoken_raw['exp'])

    def __str__(self):
        return self._msg


class CodeNotExistError(Exception):
    def __init__(self, code):
        self._msg = code

    def __str__(self):
        return self._msg


class CodeExpiredError(Exception):
    def __init__(self, spec):
        self._msg = 'code=%s, expired_date=%i'.format(
            spec['code'], spec['expired-date']
        )

    def __str__(self):
        return self._msg


class EmailExistError(Exception):
    def __init__(self, email):
        self._msg = email

    def __str__(self):
        return self._msg
