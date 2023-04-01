import re
import os
import pickle

USER_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_files')


class Container:

    def __init__(self) -> None:
        self.__data = set()

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, new_set: set):
        self.__data = new_set

    def add(self, *elems: tuple[str]):
        self.data.update(*elems)

    def remove(self, elem):
        try:
            self.data.remove(elem)
        except KeyError:
            print("No such key in container!")

    def find(self, elem):
        print("Element found!") if elem in self.data else print("Element not found!")

    def list(self) -> list:
        return list(self.data)

    def grep(self, regex):
        pattern = re.compile(regex)
        founded = []

        for element in self.data:
            if pattern.search(element):
                founded.append(element)

        return founded

    def save(self, endpoint: str):
        directory: str = os.path.join(USER_DATA_DIR, endpoint + ".pkl")

        with open(directory, 'wb+') as f:
            pickle.dump(self.data, f)

    def load(self, endpoint, switch=False):
        directory: str = os.path.join(USER_DATA_DIR, endpoint + ".pkl")

        if not os.path.lexists(directory):
            if switch:
                self.data = set()
            return

        with open(directory, 'rb') as load_file:
            try:
                new_data: set = pickle.load(load_file)

            except pickle.UnpicklingError:
                new_data = set()

        self.data = new_data

    def switch(self):
        pass
