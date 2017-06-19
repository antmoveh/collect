import logging

# def use_log(func):
#     def wrapper(*args, **kwargs):
#         logging.warning("%s is running" % func.__name__)
#         return func(*args, **kwargs)
#     return wrapper
#
def use_logging(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level ==  "warn":
                logging.warning("%s is running" % func.__name__)
            return func(*args)
        return wrapper
    return decorator

class Foo(object):
    def __init__(self, func):
        self._func = func

    def __call__(self, m):
        print(m)
        print('class decorator running')
        self._func(m)
        print('class decorator ending')


# def logged(func):
#     def with_logging(*args, **kwargs):
#         print(func.__name__ + " was called")
#         return func(*args, **kwargs)
#     return with_logging
#
@use_logging(level="warn")
def foo(name='foo'):
    print('i am %s' % name)

@Foo
def bar(m):
    print('11111111111111111111111111')

# @logged
# def f(x):
#     """does some math"""
#     return x + x * x

# print(f(4))
#bar('ba')

def pa(m):
    def deco(func):
        def wrapper(a, b):
            print(m['d'])
            print(m['f'])
            func(a, b)
        return wrapper
    return deco

@pa(m={'d':'d', 'f':'f'})
def addFunc(a, b):
    print(a + b)

addFunc(3, 8)

bar({'a':'a', 'b':'b'})




