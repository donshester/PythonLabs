from core.serializer import Serializer
def function(a, b):
    return a*b**2
def main():
    seralizer = Serializer('json')

    print(seralizer.serialize(function))


if __name__ == '__main__':
    main()