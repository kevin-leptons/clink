from wsgiref.simple_server import make_server
from clink import App
from clink.com.marker import com
from clink.marker import route
from clink.type.com import Controller
from clink.type import AppConf

# define component - application configuration
conf = AppConf('book-api')

# define component - controller
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
app = App(conf)

# add component to application
app.add_com(BookCtl)

# create instance of all of components
app.load()

# serve application
address = 'localhost'
port = 8080
print('Prepare to start on http://%s:%i' % (address, port))
httpd = make_server(address, port, app)
httpd.serve_forever()
