from smtplib import SMTP
from email.mime.text import MIMEText

from clink.com import stamp
from clink.type.com import Service
from clink.type import AppConf, AuthConf


@stamp(AppConf, AuthConf)
class SmtpSv(Service):
    '''
    Send mail message on SMTP
    '''

    def __init__(self, app_conf, auth_conf):
        '''
        :param AppConf app_conf:
        :param AuthConf auth_conf:
        '''

        self._app_conf = app_conf
        self._auth_conf = auth_conf

        self._from = '{} <{}>'.format(
            self._app_conf.name, self._auth_conf.root_email
        )

        self._smtp = self._connect()

    def send(self, dest_email, subject, text_body):
        '''
        Send plain text message

        :param str dest_email:
        :param str subject:
        :param str text_body:
        '''

        msg = MIMEText(text_body)
        msg['To'] = dest_email
        msg['Subject'] = subject
        msg['From'] = self._from

        self._smtp.sendmail(
            self._auth_conf.root_email, dest_email, msg.as_string()
        )

    def _connect(self):
        port = self._auth_conf.root_email_server_port
        smtp = SMTP(self._auth_conf.root_email_server, port)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(self._auth_conf.root_email, self._auth_conf.root_email_pwd)

        return smtp
