NODE, EDGE, ATTR = 0,1,2

class Node(object):
    def __init__(self, name, attrs={}):
        
        if not isinstance(name, str):
            raise ValueError("Node names should be a string")
        
        self.name = name
        self.attrs = attrs

    def __eq__(self, other):
        return self.name == other.name and self.attrs == other.attrs

    def __repr__(self):
        return 'Node({})'.format("'{}'".format(self.name) if not self.attrs else "'{}', {}".format(self.name,self.attrs))

class Edge(object):
    def __init__(self, src, dst, attrs={}):
        
        for x in (src,dst):
            if not isinstance(x, str):
                raise ValueError("Node names should be a string")
        
        self.src = src
        self.dst = dst
        self.attrs = attrs

    def __eq__(self, other):
        return (self.src == other.src and
                self.dst == other.dst and
                self.attrs == other.attrs)


class Graph(object):
    def __init__(self, data=[]):
        
        if not isinstance(data, list):
            raise TypeError("Should be a list of nodes, edges and attributes")
        
        self.nodes = []
        self.edges = []
        self.attrs = {}
        
        control = {0:(lambda x: Node(*x), self.nodes, 1, 2),
                   1:(lambda x: Edge(*x), self.edges, 2, 3),
                   2:(lambda x: self.attributes(*x), self.attrs, 2, 2)
                  }
        
        for x in data:
            
            if len(x) < 2:
                raise TypeError("'{}' has not enough arguments")
            
            if x[0] not in control:
                raise ValueError("{} is not in (NODE, EDGE, ATTR)".format(x[0]))
            
            function, container, min_args, max_args = control[x[0]]
            
            if not 0 < len(x[1:]) <= max_args:
                raise ValueError("To many or few arguments")
            
            if isinstance(container, list):
                container.append(function(x[1:]))               
            else:
                function(x[1:])
            
    def attributes(self, name, value):
        self.attrs[name] = value
