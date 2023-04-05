import sys

sys.path.append("../..")

from Lab2.task2.entities.terminal import Terminal


def main():
    terminal = Terminal()
    terminal.start()


if __name__ == '__main__':
    main()
