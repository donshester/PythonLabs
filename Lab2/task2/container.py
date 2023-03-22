import re


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

    def remove(self, elem):
        try:
            self.data.remove(elem)
        except KeyError:
            print("No such key in container!")

    def find(self, elem):
        return elem if elem in self.data else "Element not found!"

    def list(self) -> list:
        return list(self.data)

    def grep(self, regex):
        pattern = re.compile(regex)
        founded = []

        for element in self.data:
            if pattern.search(element):
                founded.append(element)

        return founded

    def save(self):
        pass

    def switch(self):
        pass
