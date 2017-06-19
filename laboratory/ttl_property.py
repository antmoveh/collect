from time import time


class ttl_property:

    def __init__(self, ttl=None):
        self.ttl = ttl


    def __call__(self, func):
        self.func = func
        return self


    def __get__(self, instance, owner):
        if not hasattr(instance, self.__class__.__name__):
            #setattr(instance, owner.__name__, (self.func(instance), time()))
            self.__set__(instance, self.func(instance))
        value, pre_time = getattr(instance, self.__class__.__name__)
        if time() - pre_time > self.ttl:
            value = self.func(instance)
            self.__set__(instance, value)
            # setattr(instance, owner.__name__, (value, time()))
        return value


    def __set__(self, instance, value):
        instance.__dict__[self.__class__.__name__] = (value, time())

