from clink import Router, Route


def book_handle(name):
    print('This is %s book' % name)


def hat_handle(name):
    print('This is %s hat' % name)


router = Router()

book_route = Route('get', 'text/plain', 'api/book', book_handle)
hat_route = Route('get', 'text/plain', 'api/hat', hat_handle)

router.add_route(book_route)
router.add_route(hat_route)

req_handle = router.find_handle('get', 'text/plain', 'api/book')
req_handle('story')

req_handle = router.find_handle('get', 'text/plain', 'api/hat')
req_handle('baseball')
