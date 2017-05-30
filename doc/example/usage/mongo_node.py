from pymongo import IndexModel, ASCENDING
from clink.db import MongoDocSpec, MongoNode

# sample online database, replace it with url of your database
DB_URL = 'mongodb://dev:dev@ds011158.mlab.com:11158/clink'
DB_NAME = 'clink'

# create book document specification
book_name_index = IndexModel([('name', ASCENDING), ('author', ASCENDING)])
book_doc_spec = MongoDocSpec('book', [book_name_index])

# connect to server database
# if documents can't meets requirements, it raises error
mongo_node = MongoNode(DB_URL, DB_NAME, [book_doc_spec])

# retrieve document which uses to control books
book_doc = mongo_node.doc('book')

# create new book
book_doc.insert_one({'name': 'How to Die', 'author': 'Death'})

# retrieve book
book_item = book_doc.find_one({'name': 'How to Die'})

# show book to command line
print(book_item)

# close database node
mongo_node.close()
