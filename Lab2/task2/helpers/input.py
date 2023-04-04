from Lab2.task2.constants.cli_messages import CLI_HELP


class Input:

    @classmethod
    def cmd_parse(cls, text: str):

        parsed_command = text.split()[0]
        if parsed_command == "":
            return

        if parsed_command not in CLI_HELP.keys():
            return f"{parsed_command} is unknown"
        else:
            return parsed_command

    @classmethod
    def cmd_parse_args(cls, text: str, grep: bool):

        parsed_command = text.split()[0]

        if parsed_command not in CLI_HELP.keys():
            print(f"{parsed_command} is unknown")
            return tuple()

        comm_args = text.split(' ', 1)

        if grep:
            return tuple(comm_args[1])

        args = comm_args[1].split(',')

        for arg in range(len(args)):
            args[arg] = args[arg].strip()

        args[:] = (value for value in args if value != "")

        return tuple(args)

    @classmethod
    def get_choice(cls, prompt: str):
        while True:
            choice = input(prompt)
            if choice == "y":
                return True
            elif choice == "n":
                return False
            else:
                print("\n")

    @classmethod
    def validate_username(cls, name: str):
        return all(c.isalpha() and ord(c) < 128 for c in name)