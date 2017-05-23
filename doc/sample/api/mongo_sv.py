from clink.service import MongoSv, MongoConf, MongoDocSpec
from pymongo import IndexModel, ASCENDING


conf = MongoConf('mongodb://localhost', 'book-db')
mongo_sv = MongoSv(conf)

book_doc_name = 'book'
book_doc_index_1 = IndexModel([('name', ASCENDING)], unique=True)
book_doc_spec = MongoDocSpec(book_doc_name, [book_doc_index_1])

mongo_sv.use_docspec(book_doc_spec)

book_doc = mongo_sv.doc(book_doc_name)
book_doc.insert_one({'name': 'How to Die', 'author': 'Death'})

book = book_doc.find_one({'name': 'How to Die'})
print(book)
