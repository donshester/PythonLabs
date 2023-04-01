import sys
from user import User
from constants.commands import Command
from helpers.input import Input
class Terminal:

    def __init__(self):
        self.__user = None

        try:
            self.__user = User(input('Enter username'))
        except KeyboardInterrupt:
            sys.exit()

        def start(self):
            self.__user = User(input('username'))
            while True:
                try:
                    self.__prompt = input(f"{self.__user.username}: ")
                    comm = Input.command_parse(self.__prompt)

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
                    elif comm == "whoami":
                        self.whoami_command()
                    elif comm == "exit":
                        self.exit_command()
                    else:
                        print(comm)

                except KeyboardInterrupt:
                    self.exit_command()


