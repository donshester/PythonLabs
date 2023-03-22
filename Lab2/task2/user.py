from container import Container


class User:

    def __init__(self, name) -> None:
        self._user_name = name
        self._container = Container()

    @property
    def user_name(self):
        return self._user_name

    @property
    def container(self):
        return self._container

    @user_name.setter
    def user_name(self, name):
        self.user_name = name

    def add_elements(self, *elems):
        self.container.add(elems)

    def remove_element(self, elem):
        self.container.remove(elem)

    def find_element(self, elem):
        self.container.find(elem)

    def grep_elements(self, regex):
        self.container.grep(regex)

    def list_data(self):
        print(self.container.list())

    def save(self):
        self.container.save(self.user_name)

    def load(self):
        self.container.load(self.user_name)

    def switch(self):
        pass
