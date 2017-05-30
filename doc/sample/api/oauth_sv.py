from clink.service import OAuthSv, MongoSv, AuthDbSv, AccSv, \
                          AuthConf, MongoConf


mongo_conf = MongoConf('mongodb://localhost', 'book-db')
mongo_sv = MongoSv(mongo_conf)

root_pwd = 'root-pwd'
root_email = 'root@email.com'
root_email_pwd = 'root-email-pwd'
root_email_server = 'smtp.email.com:587'
auth_conf = AuthConf(
    root_pwd, root_email, root_email_pwd, root_email_server,
    'jwt-key'
)

authdb_sv = AuthDbSv(mongo_sv)
acc_sv = AccSv(authdb_sv, auth_conf)
oauth_sv = OAuthSv(authdb_sv, acc_sv, auth_conf)

token = oauth_sv.mktoken_pwd('root', root_pwd)
for k, v in token.items():
    str_v = str(v)
    print('%s: %s...' % (k, str_v[0:32]))
