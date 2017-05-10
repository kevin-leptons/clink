from wsgiref.simple_server import make_server
from clink import Application, Route, Router

ADDRESS = 'localhost'
PORT = 8080

# create route
book_route = Route('book')


# add request handle to route
@book_route.get('item')
def get_book(req, res):
    res.body = {
        'name': 'Linux Programming Interface',
        'author': 'Michael Kerrisk'
    }


# create application
router = Router([book_route])
app = Application(router)

# serve application
print('Prepare to start on http://%s:%i' % (ADDRESS, PORT))
httpd = make_server(ADDRESS, PORT, app)
httpd.serve_forever()
