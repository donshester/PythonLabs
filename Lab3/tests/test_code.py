import math


def circle_area(r):
    return math.pi * (r ** 2)


def decorator1(func):
    def inner(*args, **kwargs):
        return func(*args, **kwargs) * 10

    return inner


@decorator1
def square_area(h):
    return h * h


def limit(n):
    def wrapper(func):
        def inner(*args, **kwargs):
            if len(args) + len(kwargs) > n:
                raise ValueError('too much arguments')
            return func(*args, **kwargs)

        return inner

    return wrapper


@limit(5)
def sum_func(*args):
    return sum(args)


def generator(start=0, stop=10):
    for i in range(start, stop):
        yield i


def subgenerator():
    yield from generator()
    yield from generator(5)
    yield from generator(5, 20)


def closure(a, b, c):
    def sum_abc():
        return a + b + c

    return sum_abc


lambda_pow = lambda x: x ** x


def factorial(n):
    return 1 if n == 0 else n * factorial(n - 1)


class A:
    def info_a(self):
        return 'a'


class B:
    def info_b(self):
        return 'b'


class C(A, B):
    def info_c(self):
        return self.info_a() + self.info_b() + 'c'


class D(C):
    def info_d(self):
        return 'd'


class E(D):
    def info_e(self):
        return 'e' + self.info_a() + \
            self.info_b() + self.info_c() + self.info_d()


class Human:
    CONST = '123ABC456'

    def __init__(self, age, name):
        self._age = age
        self._name = name

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        self._age = age

    @age.deleter
    def age(self):
        del self._age
        self._name = 'name after age deletion'

    @classmethod
    def get_const(cls):
        return cls.CONST

    @staticmethod
    def static():
        return 'It is static'


a = 5


class Brrr:
    @classmethod
    def class_meth(cls):
        return 55


class Clas(Brrr):
    def __init__(self):
        print(2)


def func1():
    global a
    a *= 2
    return a


def func2():
    x = 10

    def inner():
        nonlocal x
        x *= 20

    inner()
    return x


def func3(lst):
    return type(lst), len(lst)


it = iter(list(range(10)))
generator_expression = (i for i in range(10))

bts = "123qwe456asd".encode()
bts_arr = bytearray(bts)


def sum_args(*args):
    return sum(args)


def sum_kwargs(**kwargs):
    return sum(kwargs.values())


def sum_args_kwargs(*args, **kwargs):
    return sum_args(*args) + sum_kwargs(**kwargs) + \
        sum(args) + sum(kwargs.values())


class Profile:
    def __init__(self, age, name, email, phone):
        self.age = age
        self.name = name
        self.email = email
        self.phone = phone

    def __str__(self):
        return f'Profile: {self.age = }, {self.name = }, {self.email = }, {self.phone = }'