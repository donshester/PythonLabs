from .container import Container
from Lab2.task2.helpers.input import Input
from Lab2.task2.constants.cli_messages import  CHANGE_USER_LOAD_QUESTION


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
        self._user_name = name

    def add_elements(self, *elems):
        self.container.add(*elems)

    def remove_element(self, elem):
        return self.container.remove(elem)

    def find_element(self, elem):
        self.container.find(elem)

    def grep_elements(self, regex):
        print(self.container.grep(regex))

    def list_data(self):

        print(f"\t[{', '.join(self.container.list())}]")

    def save(self):
        self.container.save(self.user_name)

    def load(self):

        self.container.load(self.user_name)

    def switch(self, new_user_name: str):
        choice: bool = Input.get_choice(CHANGE_USER_LOAD_QUESTION)
        if choice:
            self._container.load(new_user_name, True)
        else:
            self._container.data = set()

        self.user_name = new_user_name
        print(f"\nYou switched to the user {self.user_name}.")
