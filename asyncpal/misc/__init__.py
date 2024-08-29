"""Misc functions and classes."""
import os
import sys
import time
import itertools
import functools
import logging
from traceback import format_exception
from queue import Empty as EmptyQueueError
from asyncpal import errors


__all__ = ["split_map_task", "split_starmap_task",
           "get_chunks", "Countdown", "LOGGER"]


LOGGER = logging.getLogger("asyncpal")


def ensure_args_kwargs(args=None, kwargs=None):
    args = args if args else tuple()
    kwargs = kwargs if kwargs else dict()
    return args, kwargs


def get_chunks(iterable, chunk_size):
    """
    Split an iterable into chunks

    [param]
    - iterable: the iterable to split
    - chunk_size: max length for a chunk

    [return]
    Returns an iterator
    """
    iterator = iter(iterable)
    return iter(lambda: tuple(itertools.islice(iterator, chunk_size)),
                tuple())


def drain_queue(q):
    """Private function !"""
    while True:
        try:
            q.get_nowait()
        except EmptyQueueError as e:
            break


def iterate_queue(q):
    while True:
        try:
            yield q.get_nowait()
        except EmptyQueueError as e:
            break


def get_cpu_count():
    if sys.version_info >= (3, 13):
        return os.process_cpu_count()
    else:
        return os.cpu_count()


def add(a, b):
    return a + b


class Countdown:
    """Class to continually update a timeout as time passes.
    Used a lot by pools for map operations"""
    def __init__(self, timeout):
        """Init.

        [param]
        - timeout: None or a timeout (int or float) value in seconds"""
        self._timeout = timeout
        self._instant_a = time.monotonic()
        if timeout:
            self._instant_b = self._instant_a + timeout
        else:
            self._instant_b = None

    @property
    def timeout(self):
        return self._timeout

    @property
    def instant_a(self):
        """Instant alpha: the instant the Countdown object is created"""
        return self._instant_a

    @property
    def instant_b(self):
        """Instant beta: the exact instant the timeout expires.
        Is None if the original timeout is None"""
        return self._instant_b

    @staticmethod
    def get_instant(self):
        """Returns an instant value"""
        return time.monotonic()

    def check(self):
        """Returns a new timeout value at each call"""
        if self._instant_b is None:
            return self._timeout
        x = self._instant_b - time.monotonic()
        return x if x > 0 else 0


def split_map_task(target, *iterables, chunk_size=1):
    """
    Split a map task into subtasks that don't take any arguments.
    The iterables are chunked according to chunk_size.

    [param]
    - target: the callable task
    - iterables: the map iterables to pass to target
    - chunk_size: the max length of a chunk

    [yield]
    Iteratively get a subtask that don't accept any arguments
    """
    for chunk in get_chunks(zip(*iterables), chunk_size):
        yield functools.partial(_subtask, target, chunk)


def split_starmap_task(target, iterable, chunk_size=1):
    """Split a starmap task into subtasks that don't take any arguments.
    The iterable is chunked according to chunk_size.

    [param]
    - target: the callable task
    - iterable: a sequence of tuples each representing args to pass to target
    - chunk_size: the max length of a chunk

    [yield]
    Iteratively get a subtask that don't accept any arguments
    """
    for chunk in get_chunks(iterable, chunk_size):
        yield functools.partial(_subtask, target, chunk)


def _subtask(target, chunk):
    return [target(*args) for args in chunk]


class ExceptionWrapper:
    def __init__(self, exc, tb=None):
        self._exc = exc
        tb = exc.__traceback__ if tb is None else tb
        # traceback string
        tbs = "".join(format_exception(type(exc), exc, tb))
        self._traceback_str = '\n"""\n{}"""'.format(tbs)
        # traceback objects hold references to exception frames
        # therefore, let's clear them
        exc.__traceback__ = None

    def _get_exc_chain(self):
        result = list()
        exc = self._exc
        while exc is not None:
            exc.__traceback__ = None
            cause = exc.__cause__
            if cause is None:
                if exc.__suppress_context__:
                    break
                else:
                    cause = exc.__context__
            if cause is None:
                break
            result.append(cause)
            exc = cause
        return tuple(result)

    def __reduce__(self):
        exc_chain = self._get_exc_chain()
        return _update_exc, (self._exc, self._traceback_str, exc_chain)


def _update_exc(exc, traceback_str, exc_chain):
    exc.__context__ = errors.RemoteError(traceback_str, exc_chain)
    return exc
