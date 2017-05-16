from .app import App
from .auth_routing import routes
from .auth import Auth
from .db import MongoNode
from .service import MailService


class AuthApp(App):
    def __init__(
        self, name, dburl, dbname, jwt_key, 
        root_pwd, root_email, email_pwd, email_server,
        token_time=4*3600, rtoken_time=30*24*3600
    ):
        super().__init__(name)

        self.ctx['rootmail'] = root_email
        self.ctx['dbnode'] = MongoNode(dburl, dbname)
        self.ctx['auth'] = Auth(
            self.ctx['dbnode'], root_pwd, root_email,
            jwt_key, token_time, rtoken_time
        )
        self.ctx['mailsv'] = MailService(
            email_server, root_email, email_pwd, name
        )
        self.router.add_routes(routes)
