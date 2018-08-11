# Python 3.6

calls = set()

class InputCell(object):
    def __init__(self, initial_value):
        self.__val = initial_value
        
    @property
    def value(self):
        return self.__val
    
    @value.setter
    def value(self, value):
        if self.__val != value:
            self.__val = value      
            for call in calls:
                call.update()

class ComputeCell(object):
    def __init__(self, inputs, compute_function):    
        self.input = inputs
        self.funct = compute_function
        self.__val = self.funct([x.value for x in self.input])
        self.observors = set()
        calls.add(self)
        
    @property
    def value(self):
        return self.funct([x.value for x in self.input])

    def update(self):
        for y in self.observors:
            if self.value != self.__val:
                y(self.value)
    
    def add_callback(self, callback):
        self.observors.add(callback)

    def remove_callback(self, callback):
        self.observors -= {callback}