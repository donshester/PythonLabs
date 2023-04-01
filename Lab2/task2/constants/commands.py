from enum import Enum


class Command(Enum):
    add = "add"
    remove = "remove"
    find = "find"
    list = "list"
    grep = "grep"
    save = "save"
    load = "load"
    switch = "switch"
