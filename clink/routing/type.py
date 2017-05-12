'''
SYNOPSIS
    class RouteNode
    class RouteSpec

DESCRIPTION

    Data structures are uses during routing.
'''


class RouteNode():
    def __init__(self, name):
        self.name = name
        self.child = {}
        self.specs = []


class RouteSpec():
    def __init__(self, method, path, handler, req_type):
        self.method = method
        self.path = path
        self.handler = handler
        self.req_type = req_type
