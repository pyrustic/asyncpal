import time


def divide(a, b, sleep=0):
    if sleep:
        time.sleep(sleep)
    return a/b


def add(a, b, sleep=0):
    if sleep:
        time.sleep(sleep)
    return a + b


def square(x, sleep=0):
    if sleep:
        time.sleep(sleep)
    return x**2


def get_worker_exception(pool):
    try:
        pool.check()
    except Exception as e:
        return e
