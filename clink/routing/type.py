class CtlMethod():
    '''
    Specify controller method
    '''

    def __init__(self, path, method, req_type):
        '''
        :param str path:
        :param clink.type.HttpMethod method:
        :param str req_type:
        '''

        self.path = path
        self.method = method
        self.req_type = req_type
