from Lab2.task2.constants.commands import Command

CLI_HELP = {
    Command.add.value: "add one or more elements to the container ",
    Command.remove.value: "delete key from container",
    Command.list.value: "print all elements of container",
    Command.find.value: "check if the element is presented in the container",
    Command.grep.value: "<regex> – check the value in the container by regular expression",
    Command.save.value: "save container to file",
    Command.load.value: "load container from file",
    Command.switch.value: "switches to another user",
    Command.exit.value: "exit program",
    Command.help.value: "shows commands"
}

CHANGE_USER_SAVE_QUESTION: str = "\nWould you like to save your data before change the user? [y/n]: "
CHANGE_USER_LOAD_QUESTION: str = "\nWould you like to load your data before change the user? [y/n]: "
EXIT_USER_SAVE_QUESTION: str = "\nWould you like to load your data before exit? [y/n]: "
ARGUMENT_EXPECTED: str = "\nOnly one argument expected!"
