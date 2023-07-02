from functools import wraps
from time import time


class AppRoute:
    def __init__(self, routes, url):

        self.routes = routes
        self.url = url

    def __call__(self, cls):

        self.routes[self.url] = cls()


def app_route(routes, url):
    def decorator(func):
        routes[url] = func

        @wraps(func)
        def decorated(*args, **kwargs):
            res = func(*args, **kwargs)
            return res
        return decorated
    return decorator


class DebugClass:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):

        def timeit(method):
            def timed(*args, **kwargs):
                ts = time()
                result = method(*args, **kwargs)
                te = time()
                delta = te - ts

                print(f'debug --> {self.name} выполнялся {delta*100:2.2f}e+2 ms')
                return result

            return timed

        return timeit(cls)


def debug_func(name):
    def decorator(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            ts = time()
            res = func(*args, **kwargs)
            te = time()
            delta = te - ts

            print(f'debug --> {name} выполнялся {delta*100:2.2f}e+2 ms')
            return res
        return decorated
    return decorator

