from clink.service import AuthDbSv, MongoSv, MongoConf


mongo_conf = MongoConf('mongodb://localhost', 'book-db')
mongo_sv = MongoSv(mongo_conf)

authdb_sv = AuthDbSv(mongo_sv)
print(authdb_sv.acc_doc())
print(authdb_sv.grp_doc())
print(authdb_sv.rpwd_doc())
print(authdb_sv.acctmp_doc())
