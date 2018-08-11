NODE, EDGE, ATTR = 0,1,2

class Schema_object(object):    
    @classmethod
    def validate(cls, args):
        return all(isinstance(arg_,type_) for arg_,type_ in zip(args, cls._schema) if type_)

class Node(Schema_object):
    _schema = (str, dict)               
    def __init__(self, name, attrs={}):      
        self.name = name
        self.attrs = attrs

    def __eq__(self, other):
        return self.name == other.name and self.attrs == other.attrs

class Edge(Schema_object):
    _schema = (str,str,dict)
    def __init__(self, src, dst, attrs={}):
        self.src = src
        self.dst = dst
        self.attrs = attrs

    def __eq__(self, other):
        return self.src == other.src and self.dst == other.dst and self.attrs == other.attrs

class Attr(Schema_object):
    _schema = (str,None)
    def __init__(self, key, value):
        self.key_value = (key,value)
                   
class Graph(object):
    def __init__(self, data=[]):
        
        self.nodes = []
        self.edges = []
        self._attrs = []
        
        control = {0: (Node, self.nodes),
                   1: (Edge, self.edges),
                   2: (Attr, self._attrs)
                  }
        
        for x in data:
            
            if not isinstance(x, tuple) or len(x) < 2:
                raise TypeError("'{}' has invalid format".format(x))
            
            if x[0] not in control:
                raise ValueError("'{}' is an unkonwn data type".format(x))
                
            cls, container = control[x[0]]
            args = x[1:]

            if not cls.validate(args):
                raise ValueError("'{}' has an invalid schema".format(x))
            
            container.append(cls(*args))
            
    @property
    def attrs(self):
        return dict(a.key_value for a in self._attrs)