from clink import Router, Route, Request


def book_handle(name):
    print('This is %s book' % name)


def hat_handle(name):
    print('This is %s hat' % name)


router = Router()

book_route = Route('/api/book', 'get', 'text/plain', book_handle)
hat_route = Route('/api/hat', 'get', 'text/plain', hat_handle)

router.add_route(book_route)
router.add_route(hat_route)

req = Request()
req.method = 'get'
req.content_type = 'text/plain'

req.path = '/api/book'
req_handle = router.handle(req)
req_handle('story')

req.path = '/api/hat'
req_handle = router.handle(req)
req_handle('baseball')
