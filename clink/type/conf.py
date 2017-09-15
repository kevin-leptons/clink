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
    '''
    Authorization configuration
    '''

    def __init__(
        self, root_pwd, root_email, root_email_pwd, root_email_server,
        root_email_server_port, jwt_key, 
        token_time=4*3600, rtoken_time=30*24*3600
    ):
        '''
        :param str root_pwd:
        :param str root_email:
        :param str root_email_pwd:
        :param str root_email_server:
        :param int root_email_server_port:
        :param str jwt_key:
        :param int token_time:
        :param int rtoken_time:
        '''

        self.root_pwd = root_pwd
        self.root_email = root_email
        self.root_email_pwd = root_email_pwd
        self.root_email_server = root_email_server
        self.root_email_server_port = root_email_server_port
        self.jwt_key = jwt_key
        self.token_time = token_time
        self.rtoken_time = rtoken_time
