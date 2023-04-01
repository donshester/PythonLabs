class Container:

    def __init__(self) -> None:
        self.__data = set()

    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, new_set: set):
        self.__data = new_set

    def add(self, *elems):
        self.data.add(*elems)
    
    def remove(self):
        pass


    def find(self):
        pass
        
    def list(self):
        pass 
    def save(self):
        pass
        
    def switch(self):
        pass
