'''
Models is related with account management
'''

from .std import acc_name, acc_pwd, email, phone, objectid, unix_time


# database model

#:
confirm_code = {
    'type': 'string',
    'pattern': '^([a-zA-Z]{4}-){3}[a-zA-Z]{4}$'
}

# front models

#:
get_me_body = {
    'type': 'object',
    'required': [
        '_id', 'name', 'email', 'phone',
        'created_date', 'modified_date', 'last_action'
    ],
    'properties': {
        '_id': objectid,
        'name': acc_name,
        'email': email,
        'phone': phone,
        'created_date': unix_time,
        'modified_date': unix_time,
        'last_action': {'type': 'string'}
    }
}

#:
post_reg_code_body = {
    'type': 'object',
    'required': ['name', 'email', 'pwd'],
    'properties': {
        'name': acc_name,
        'pwd': acc_pwd,
        'email': email,
        'phone': phone
    }
}

#:
post_reg = {
    'type': 'object',
    'required': ['code'],
    'properties': {
        'code': confirm_code
    }
}

#:
put_pwd = {
    'type': 'object',
    'required': ['old_pwd', 'new_pwd'],
    'properties': {
        'old_pwd': acc_pwd,
        'new_pwd': acc_pwd
    }
}

#:
post_rpwd_code = {
    'type': 'object',
    'required': ['email'],
    'properties': {
        'email': email
    }
}

#:
post_rpwd = {
    'type': 'object',
    'required': ['code', 'new_pwd'],
    'properties': {
        'code': confirm_code,
        'new_pwd': acc_pwd
    }
}
