from clink.service import SmtpSv, AuthConf
from clink import AppConf


app_conf = AppConf('Awesome Application')

sender_email = 'you@email.com'
sender_email_password = 'secret-words'
email_server_address = 'smtp.email.com'
email_server_port = 587
auth_conf = AuthConf(
    'root-pwd', sender_email, sender_email_password,
    email_server_address, email_server_port, 'jwt-key'
)

smtp = SmtpSv(app_conf, auth_conf)

receiver = 'someone@email.com'
subject = 'Let be friends'
content = 'Hello there'
smtp.send(receiver, subject, content)
