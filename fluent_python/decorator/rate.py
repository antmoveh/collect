from fluent_python.decorator.ratelimit import RateLimiter


def callback(value):
    """ value 表示还需要等待多久才能下次执行"""
    print("callback")


@RateLimiter(max_calls=10, period=1, callback=callback)
def func1():
    print("func1")


def func2():
    print("func2")


if __name__ == "__main__":
 #   func1()

    with RateLimiter(max_calls=4, period=1, callback=callback) as r:
        print(type(r))
        import time
        for i in range(11):
            if not r.exceed:
                time.sleep(.4)
                func2()