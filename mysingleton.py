class Singleton(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance


class Singleton2(type):
    _inst = {}

    def __call__(self, *args, **kwargs):
        if self not in self._inst:
            self._inst[self] = super(Singleton2, self).__call__(*args, **kwargs)
        return self._inst[self]


def singleton3(cls, *args, **kwargs):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton


class MyClass(Singleton):
    a = 1

class MyClass2(metaclass=Singleton2):
    a = 1


@singleton3
class MyClass3:
    a = 1

one = MyClass()
two = MyClass()

print(id(one))
print(id(two))
print(one == two)
print(one is two)


one2 = MyClass2()
two2 = MyClass2()

print(id(one2))
print(id(two2))
print(one2 == two2)
print(one2 is two2)


one3 = MyClass3()
two3 = MyClass3()
print(id(one3))
print(id(two3))
print(one3 == two3)
print(one3 is two3)