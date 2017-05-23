# STEP 1: get clink library
from clink import stamp, mapper, App, AppConf, Controller
from clink.validator import reqv

# STEP 2: get an WSGI server
from wsgiref.simple_server import make_server

# STEP 3: create application configuration and application
conf = AppConf('book-api', 'Hell Corporation', '1st, Hell street')
app = App(conf)

# STEP 4: define component - controllers
#===[BEGIN] TRY DATA VALIDATION ==============================================
POST_BOOK_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'required': ['name', 'author'],
    'properties': {
        'name': {'type': 'string', 'pattern': '^[a-zA-Z0-9 ]{2,32}$'},
        'author': {'type': 'string', 'pattern': '^[a-zA-Z0-9 ]{2,16}$'},
        'notes': {'type': 'string', 'pattern': '^.{0,1024}$'}
    }
}

@stamp()
@mapper.path('book')
class BookCtl(Controller):
    @mapper.post('item')
    @reqv.body(POST_BOOK_SCHEMA)
    @reqv.max_content_size(50)
    def get_item(self, req, res):
        res.body = {'msg': 'created'}
#===[END] TRY DATA VALIDATION ================================================

# STEP 5: add components to application
app.add_com(BookCtl)

# STEP 6: load components
app.load()

# STEP 7: serve application on WSGI server
address = 'localhost'
port = 8080
print('Prepare API on http://%s:%i/book/item' % (address, port))
httpd = make_server(address, port, app)
httpd.serve_forever()
