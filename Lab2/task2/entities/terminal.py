import sys
from Lab2.task2.entities.user import User
from Lab2.task2.helpers.input import Input
from Lab2.task2.constants.cli_messages import ARGUMENT_EXPECTED, CHANGE_USER_SAVE_QUESTION, CLI_HELP


class Terminal:

    def __init__(self):
        self.__prompt = None
        self.__user = None

        try:
            self.__user = User(input('Enter username: '))
        except KeyboardInterrupt:
            sys.exit()

    def start(self):

        while True:
            self.__prompt = input(f"[{self.__user.user_name}]: ")
            comm = Input.cmd_parse(self.__prompt)
            if comm == "add":
                self.add_command()
            elif comm == "remove":
                self.remove_command()
            elif comm == "find":
                self.find_command()
            elif comm == "list":
                self.list_command()
            elif comm == "grep":
                self.grep_command()
            elif comm == "save":
                self.save_command()
            elif comm == "load":
                self.load_command()
            elif comm == "switch":
                self.switch_command()
            elif comm == "exit":
                self.exit_command()
            elif comm == "help":
                self.help_command()
            else:
                print(comm)

    def add_command(self):
        args = Input.cmd_parse_args(self.__prompt, False)
        if len(args) == 0:
            print("No arguments to add!")
            return
        self.__user.add_elements(args)

    def remove_command(self):
        args = Input.cmd_parse_args(self.__prompt, False)

        if len(args) == 0:
            print("No arguments to remove!")
            return
        elif len(args) == 1:
            self.__user.remove_element(args[0])
        else:
            print(ARGUMENT_EXPECTED)

    def find_command(self):
        args = Input.cmd_parse_args(self.__prompt, False)

        if len(args) == 1:
            self.__user.find_element(args[0])
        else:
            print(ARGUMENT_EXPECTED)

    def list_command(self):
        self.__user.list_data()

    def grep_command(self):
        args = Input.cmd_parse_args(self.__prompt, True)
        if len(args) != 0:
            self.__user.grep_elements(''.join(args))
        else:
            print("No matches found!")

    def save_command(self):
        self.__user.save()

    def load_command(self):
        self.__user.load()

    def switch_command(self):
        args = Input.cmd_parse_args(self.__prompt, False)

        if len(args) == 1 and Input.validate_username(args[0]):
            choice: bool = Input.get_choice(CHANGE_USER_SAVE_QUESTION)
            if choice:
                self.__user.save()
            self.__user.switch(args[0])
        elif len(args) != 1:
            print(ARGUMENT_EXPECTED)
        else:
            print("Incorrect username!")

    def exit_command(self):
        choice: bool = Input.get_choice(CHANGE_USER_SAVE_QUESTION)
        if choice:
            self.__user.save()
        sys.exit()

    @staticmethod
    def help_command():
        print("\nAvailable commands:")
        for command, help_text in CLI_HELP.items():
            print(f"{command}: {help_text}")
        print('\n')
