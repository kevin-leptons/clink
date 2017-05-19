import random
from hashlib import sha224
from string import ascii_lowercase, ascii_uppercase, digits

_PWD_CHARS = ascii_lowercase + ascii_uppercase + digits
_CODE_CHARS = ascii_uppercase


def hash_pwd(password):
    return sha224(password.encode('utf-8')).hexdigest()


def rand_pwd():
    return ''.join(random.sample(_PWD_CHARS, 6))


def rand_code():
    a = ''.join(random.sample(_CODE_CHARS, 4))
    b = ''.join(random.sample(_CODE_CHARS, 4))
    c = ''.join(random.sample(_CODE_CHARS, 4))
    d = ''.join(random.sample(_CODE_CHARS, 4))

    return '-'.join([a, b, c, d])
