import argparse

from config import load_config
from core.factory import Factory
from core.serializers.jsonserializer import JSONSerializer
from core.serializers.xmlserializer import XMLSerializer
import math


def my_decor(meth):
    def inner(*args, **kwargs):
        print('I am in my_decor')
        return meth(*args, **kwargs)

    return inner


class A:
    x = 10

    @my_decor
    def my_sin(self, c):
        return math.sin(c * self.x)

    @staticmethod
    def stat():
        return 145

    def __str__(self):
        return 'AAAAA'

    def __repr__(self):
        return 'AAAAA'


class B:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    @property
    def prop(self):
        return self.a * self.b

    @classmethod
    def class_meth(cls):
        return math.pi


class C(A, B):
    pass


ser = Factory.create_serializer('json')

var = 15
var_ser = ser.dumps(var)
var_des = ser.loads(var_ser)
print(var_des)

C_ser = ser.dumps(C)
C_des = ser.loads(C_ser)

c = C(1, 2)
c_ser = ser.dumps(c)
c_des = ser.loads(c_ser)

print(c_des)
print(c_des.x)
print(c_des.my_sin(10))
print(c_des.prop)
print(C_des.stat())
print(c_des.class_meth())


def f(a):
    for i in a:
        yield i


g = f([1, 2, 3])
print(next(g))
g_s = ser.dumps(g)
g_d = ser.loads(g_s)
print(next(g_d))


def a(x):
    yield x[0]
    x[1] += 2
    yield


func = lambda x: x*x

ser = Factory.create_serializer('json')

a = ser.dumps(func)
b= ser.loads(a)

print(b(5))
#
# def main():
#     parser = argparse.ArgumentParser(description="Serializer Utility")
#     parser.add_argument("--config", help="Path to the configuration file")
#     parser.add_argument("file_from", help="Path to the input file")
#     parser.add_argument("file_to", help="Path to the output file")
#     parser.add_argument("format_from", help="Input format (json/xml)")
#     parser.add_argument("format_to", help="Output format (json/xml)")
#
#     args = parser.parse_args()
#
#     if args.config:
#         file_from, file_to, format_from, format_to = load_config(args.config)
#     else:
#         file_from = args.file_from
#         file_to = args.file_to
#         format_from = args.format_from
#         format_to = args.format_to
#
#     serializer = Factory.create_serializer(format_from)
#
#     if format_to == "json":
#         if format_from == "json":
#             data = serializer.load(file_from)
#             serializer.dump(data, file_to)
#         elif format_from == "xml":
#             data = XMLSerializer.load(file_from)
#             JSONSerializer.dump(data, file_to)
#     elif format_to == "xml":
#         if format_from == "json":
#             data = JSONSerializer.load(file_from)
#             XMLSerializer.dump(data, file_to)
#         elif format_from == "xml":
#             data = serializer.load(file_from)
#             serializer.dump(data, file_to)
#
#     print("Operation completed successfully.")


# if __name__ == '__main__':
#     main()
