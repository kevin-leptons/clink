from clink.service import AccSv, AuthDbSv, MongoSv, MongoConf
from clink import AuthConf


mongo_conf = MongoConf('mongodb://localhost', 'book-db')
mongo_sv = MongoSv(mongo_conf)

authdb_sv = AuthDbSv(mongo_sv)

root_pwd = 'root-pwd'
root_email = 'root@mail.com'
root_email_pwd = 'root-email-pwd'
root_email_server = 'smtp.email.com:578'
auth_conf = AuthConf(
    root_pwd, root_email, root_email_pwd, root_email_server,
    'jwt-key'
)

acc_sv = AccSv(authdb_sv, auth_conf)

root_acc = acc_sv.find_pwd('root', root_pwd)
print(root_acc['name'], root_acc['email'], root_acc['last_action'])
