from clink.dflow import verify, FormatError


name_schema = {'type': 'string', 'pattern': '^[a-z0-9-]{2,32}$'}
password_schema = {'type': 'string', 'pattern': '^.{6,32}$'}
info_schema = {
    'type': 'object',
    'properties': {
        'name': name_schema,
        'password': password_schema
    }
}


@verify(name_schema, password_schema)
def create_account(name, password):
    print('name=%s, password=%s, validated' % (name, password))


try:
    create_account('kevin', 'secret-words')
    create_account('ke vin', 'secret-words')
except FormatError as e:
    print('FormatError:', e)
