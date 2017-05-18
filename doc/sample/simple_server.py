from wsgiref.simple_server import make_server
from clink import App
from clink.com.marker import com
from clink.marker import route
from clink.type.com import Controller
from clink.type import AppConfig

ADDRESS = 'localhost'
PORT = 8080


@com()
@route.path('book')
class BookCtl(Controller):
    @route.get('item')
    def get_item(self, req, res):
        res.body = {
            'name': 'Linux Programming Interface',
            'author': 'Michael Kerrisk'
        }

# create application
conf = AppConfig('book-api')
app = App(conf)
app.add_com(BookCtl)
app.load()

# serve application
print('Prepare to start on http://%s:%i' % (ADDRESS, PORT))
httpd = make_server(ADDRESS, PORT, app)
httpd.serve_forever()
