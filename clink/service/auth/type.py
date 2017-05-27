class ConfirmCodeSpec():
    '''
    Specify confirm code and expired date
    '''

    def __init__(self, code, exp_date):
        '''
        :param str code:
        :param datetime exp_date:
        '''

        self.code = code
        self.exp_date = exp_date
