from clink.com import Primitive, stamp
from .version import Version


@stamp()
class AppConf(Primitive):
    '''
    Essential information about application
    '''

    def __init__(
        self, name, license='?', version=Version(0, 1, 0), 
        org_name='?', org_addr='?'
    ):
        '''
        :param str name:
        :param str license:
        :param Version version:
        :param str org_name:
        :param str org_addr:
        '''

        self.name = name
        self.license = license
        self.version = version
        self.org_name = org_name
        self.org_addr = org_addr


@stamp()
class AuthConf(Primitive):
    def __init__(
        self, root_pwd, root_email, root_email_pwd, root_email_server,
        jwt_key, token_time=4*3600, rtoken_time=30*24*3600
    ):
        self.root_pwd = root_pwd
        self.root_email = root_email
        self.root_email_pwd = root_email_pwd
        self.root_email_server = root_email_server
        self.jwt_key = jwt_key
        self.token_time = token_time
        self.rtoken_time = rtoken_time
