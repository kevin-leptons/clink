from clink import App, AppConf, com, route, Controller
from wsgiref.simple_server import make_server

conf = AppConf('book-api', 'Hell Corporation', '1st, Hell street')
app = App(conf)

@com()
@route.path('book')
class BookCtl(Controller):
    @route.get('item')
    def get_item(self, req, res):
        res.body = {
            'name': 'How to Die',
            'author': 'Death'
        }

app.add_com(BookCtl)
app.load()

address = 'localhost'
port = 8080
print('Prepare API on http://%s:%i/book/item' % (address, port))
httpd = make_server(address, port, app)
httpd.serve_forever()
