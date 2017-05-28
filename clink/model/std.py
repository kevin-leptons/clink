'''
Standard data models
'''

#:
unix_time = {'type': 'number'}
#:
objectid = {'type': 'string', 'pattern': '^[a-fA-F0-9]{24}$'}
#:
acc_name = {'type': 'string', 'pattern': '^[a-z0-9-]{2,32}$'}
#:
acc_pwd = {'type': 'string', 'pattern': '^.{6,32}$'}
#:
email = {
    'type': 'string',
    'pattern': (
        '^[a-zA-Z0-9-._]{1,64}\@'
        '[a-zA-Z0-9\[]{1}[a-zA-Z0-9.-:]{1,61}[a-zA-Z0-9\]]{1}$'
    )
}
#:
phone = {
    'type': ['string', 'null'],
    'pattern': '^\+[0-9]{2}\s[0-9]{3}\s([0-9]{3}|[0-9]{4})\s[0-9]{4}$'
}
