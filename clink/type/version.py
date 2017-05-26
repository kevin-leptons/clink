class Version():
    '''
    Strict version
    '''

    def __init__(self, major, minor, rev):
        '''
        :param int major:
        :param int minor:
        :param int rev:
        '''

        self.major = major
        self.minor = minor
        self.rev = rev

    def __str__(self):
        return '%s.%s.%s' % (self.major, self.minor, self.rev)
