from clink.type.com import Service
from clink.com.marker import com
from clink.auth import Auth
from clink.ske.auth.type import AuthConfig


@com(AuthConfig)
class AuthService(Service):
    def __init__(self, auth_conf):
        pass
