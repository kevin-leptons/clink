from smtplib import SMTP
from email.mime.text import MIMEText


class MailService():
    def __init__(self, server_addr, username, password, msg_from):
        self._server_addr = server_addr
        self._username = username
        self._password = password
        self._from = msg_from

        self._smtp = self._connect()

    def send(self, dest, subject, text_body):
        msg = MIMEText(text_body)
        msg['To'] = dest
        msg['Subject'] = subject
        msg['From'] = '%s <%s>' % (self._from, self._username)

        self._smtp.sendmail(self._username, dest, msg.as_string())

    def _connect(self):
        smtp = SMTP(self._server_addr)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(self._username, self._password)

        return smtp
