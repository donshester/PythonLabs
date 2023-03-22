from user import User
from container import Container

def main():
    user = User('vlad')

    user.load()
    user.list_data()

if __name__ == '__main__':
    main()
