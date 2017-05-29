'''
Authentication model
'''

from .std import acc_name, acc_pwd


#:
post_token_pwd = {
    'type': 'object',
    'required': ['grant_type', 'username', 'password'],
    'properties': {
        'grant_type': {'type': 'string', 'pattern': '^password$'},
        'username': acc_name,
        'password': acc_pwd
    }
}

#:
post_token_rtoken = {
    'type': 'object',
    'required': ['grant_type', 'refresh_token'],
    'properties': {
        'grant_type': {'type': 'string', 'pattern': '^refresh_token$'},
        'refresh_token': {'type': 'string'}
    }
}

#:
res_bearer_token = {
    'type': 'object',
    'required': ['token_type', 'expires_in', 'access_token', 'refresh_token'],
    'properties': {
        'token_type': {'type': 'string', 'pattern': 'Bearer'},
        'expires_in': {'type': 'number'},
        'access_token': {'type': 'string'},
        'refresh_token': {'type': 'string'},
    }
}
