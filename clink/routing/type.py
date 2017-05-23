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


class NodeAction():
    '''
    Specify pair of method, content type and handle in a map node
    '''

    def __init__(self, method, content_type, handle):
        '''
        :param str method:
        :param str content_type:
        :param function handle:
        '''

        self.method = method
        self.content_type = content_type
        self.handle = handle


class MapNode():
    '''
    Specify a map node with name, children and actions
    '''

    def __init__(self, name, child={}, actions=[]):
        '''
        :param str name:
        :param list[MapNode] child:
        :param list[NodeAction] actions:
        '''

        self.name = name
        self.child = {}
        self.actions = []
