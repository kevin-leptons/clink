from clink.service import AuthDbSv, MongoSv, MongoConf, DOC_NAMES


mongo_conf = MongoConf('mongodb://localhost', 'book-db')
mongo_sv = MongoSv(mongo_conf)

authdb_sv = AuthDbSv(mongo_sv)

for doc_name in DOC_NAMES:
    doc = authdb_sv.doc(doc_name)
    print(doc.__class__, doc.name)
