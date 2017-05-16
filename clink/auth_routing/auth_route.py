from ..routing import Route


route = Route('auth')


@route.post('token')
def get_token(req, res, ctx):
    auth = ctx['auth'].auth
    info = req.body

    res.body = auth.mktoken_pwd(info['name'], info['password'])
