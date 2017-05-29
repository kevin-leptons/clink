# STEP 1: get clink library
from clink import stamp, mapper, App, AppConf, Controller, Service
from clink.dflow import verify


# STEP 2: get an WSGI server
from wsgiref.simple_server import make_server


# STEP 3: create application configuration and application
conf = AppConf('book-api', 'Hell Corporation', '1st, Hell street')
app = App(conf)


# STEP 4: define component - service, controllers
# ===[BEGIN] TRY DATA VALIDATION =============================================
POST_BOOK_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'required': ['name', 'author'],
    'properties': {
        'name': {'type': 'string', 'pattern': '^[a-zA-Z0-9 ]{2,32}$'},
        'author': {'type': 'string', 'pattern': '^[a-zA-Z0-9 ]{2,16}$'}
    }
}


@stamp()
class BookSv(Service):
    @verify(None, POST_BOOK_SCHEMA)
    def create_one(self, book):
        # if data is invalid, clink.dflow.FormatError will be raise
        # then application catch and handle it

        pass


@stamp(BookSv)
@mapper.path('book')
class BookCtl(Controller):
    def __init__(self, book_sv):
        self._book_sv = book_sv

    @mapper.post('item')
    def create_one_book(self, req, res):
        self._book_sv.create_one(req.body)
        res.body = {'message': 'created'}
# ===[END] TRY DATA VALIDATION ===============================================


# STEP 5: add components to application
app.add_ctl(BookCtl)


# STEP 6: load components
app.load()


# STEP 7: serve application on WSGI server
address = 'localhost'
port = 8080
print('Prepare API on http://%s:%i/book/item' % (address, port))
httpd = make_server(address, port, app)
httpd.serve_forever()
