from laboratory.ttl_property import ttl_property


class Book:

    def __init__(self):
        self._price = 100.0

    @ttl_property(ttl=2)
    def price(self):
        self._price = self._price * 0.8
        return self._price



b = Book()

print(b.price)
import time
time.sleep(1)

print(b.price)

time.sleep(2)
print(b.price)
print(b.price)
time.sleep(3)
print(b.price)




