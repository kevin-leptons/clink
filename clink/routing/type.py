class CtlMethod():
    '''
    Specify controller method
    '''

    def __init__(self, method, path, content_type):
        '''
        :param str method:
        :param str path:
        :param str content_type:
        '''

        self.method = method
        self.path = path
        self.content_type = content_type
