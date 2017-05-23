from clink.com import Component, stamp


@stamp()
class AppConf(Component):
    def __init__(self, name, org_name=None, org_loc=None):
        self.name = name
        self.org_name = org_name
        self.org_loc = org_loc


@stamp()
class AuthConf(Component):
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


