# STEP 1: get clink library
from clink import stamp, mapper, App, AppConf, Controller


# STEP 2: get an WSGI server
from wsgiref.simple_server import make_server


# STEP 3: create application configuration and application
conf = AppConf('book-api', 'Hell Corporation', '1st, Hell street')
app = App(conf)


# STEP 4: define component - controllers
@stamp()
@mapper.path('book')
class BookCtl(Controller):
    @mapper.get('item')
    def get_item(self, req, res):
        res.body = {
            'name': 'How to Die',
            'author': 'Death'
        }

# ===[BEGIN] ADD MORE ROUTES HERE ============================================
    @mapper.post('item', 'text/plain')
    def create_item(self, req, res):
        res.body = {'msg': 'created'}

    @mapper.patch('item')
    def patch_item(self, req, res):
        res.body = {'msg': 'patched'}

    @mapper.put('item')
    def put_item(self, req, res):
        res.body = {'msg': 'putted'}

    @mapper.delete('item')
    def delete_item(self, req, res):
        res.body = {'msg': 'deleted'}
# ===[END] ADD MORE ROUTES HERE ==============================================


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
