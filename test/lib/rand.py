import random
from string import ascii_lowercase, ascii_uppercase, digits, printable
from faker import Faker


class Rand():
    _GROUP_CHARS = ascii_lowercase + ascii_uppercase + digits
    _STR_CHARS = printable

    def __init__(self):
        self._faker = Faker()

    def email(self):
        return self._faker.email()

    def username(self):
        return self._faker.name().lower().replace(' ', '-').replace('.', '-')

    def password(self):
        return self.username()

    def group(self):
        return ''.join(random.sample(self._GROUP_CHARS, 6))

    def string(self, len=16):
        return ''.join(random.sample(self._STR_CHARS, len))
