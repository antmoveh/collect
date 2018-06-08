# -*- coding:utf-8 -*-

import collections
import functools
import time


class RateLimiter(object):

    def __init__(self, max_calls, period=1.0, callback=None):
        print("__init__")
        self.calls = collections.deque()
        self.period = period
        self.max_calls = max_calls
        self.callback = callback

    def __call__(self, f):
        print("__call__")

        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            with self:
                if not self.exceed:
                    return f(*args, **kwargs)
                raise Exception("rate exceed")
        return wrapped

    def __enter__(self):
        print("__enter__")
        # TODO
        return self



    def __exit__(self, exc_type, exc_val, exc_tb):
        print("__exit__")
        self.calls.append(time.time())
        while self._timespan >= self.period:
            self.calls.popleft()

    @property
    def _timespan(self):
        try:
            return self.calls[-1] - self.calls[0]
        except IndexError:
            return float(0)

    @property
    def exceed(self):
        return len(self.calls) > self.max_calls

