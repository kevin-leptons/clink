# STEP 1: get clink library
from clink import stamp, mapper, App, AppConf, Controller


# STEP 2: get an WSGI server
from wsgiref.simple_server import make_server


# STEP 3: create application 
conf = AppConf('book-api')
app = App(conf)


# STEP 4: define controller
@stamp()
@mapper.path('book')
class BookCtl(Controller):
    @mapper.get('item')
    def get_item(self, req, res):
        res.body = {
            'name': 'How to Die',
            'author': 'Death'
        }


# STEP 5: add controller to application
app.add_ctl(BookCtl)


# STEP 6: load components
app.load()


# STEP 7: serve application on WSGI server
address = 'localhost'
port = 8080
print('Prepare API on http://%s:%i/book/item' % (address, port))
httpd = make_server(address, port, app)
httpd.serve_forever()
