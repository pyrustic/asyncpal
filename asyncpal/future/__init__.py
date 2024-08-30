"""In this module are defined the `Future` and the `FutureFilter`
classes as well as the `wait`, `collect`, and `as_done` functions"""
import functools
import time
import threading
from enum import Enum, unique
from queue import SimpleQueue, Empty as EmptyQueue
from asyncpal import errors, misc


__all__ = ["Future", "FutureFilter", "Status", "wait", "collect", "as_done"]


def wait(futures, timeout=None):
    """
    Wait (blocking) for futures to get done (completed, failed, or cancelled).

    [param]
    - futures: sequence of Future objects
    - timeout: None or a timeout value (int or float) in seconds.

    [return]
    Returns True if all Futures are done in the provided timeout range.
    """
    countdown = misc.Countdown(timeout)
    for future in futures:
        if timeout is None:
            new_timeout = None
        else:
            new_timeout = countdown.check()
        if not future.wait(new_timeout):
            return False
    return True


def collect(futures, timeout=None):
    """
    Collect the results of a sequence of futures.
    Beware, remote exceptions as well as CancelledError,
    or TimeoutError exceptions might be raised.

    [param]
    - futures: sequence of Future objects
    - timeout: None or a timeout value (int or float) in seconds.

    [return]
    Returns a tuple containing the ordered results
    collected from all the futures

    [except]
    - TimeoutError: raised when timeout expires
    - CancelledError: raised when a task got cancelled
    """
    result = list()
    countdown = misc.Countdown(timeout)
    for future in futures:
        if timeout is None:
            new_timeout = None
        else:
            new_timeout = countdown.check()
        result.append(future.collect(new_timeout))
    return tuple(result)


def as_done(futures, keep_order=False, timeout=None):
    """
    Yields futures iteratively as they are done

    [param]
    - futures: sequence of futures
    - keep_order: boolean to tell whether the results should be ordered or not
    - timeout: None or a timeout value (int or float) in seconds.

    [except]
    - TimeoutError: raised when timeout expires
    """
    if keep_order:
        countdown = misc.Countdown(timeout)
        for future in futures:
            if timeout is None:
                new_timeout = None
            else:
                new_timeout = countdown.check()
            if not future.wait(new_timeout):
                raise TimeoutError
            yield future
    else:
        future_filter = FutureFilter(futures)
        yield from future_filter.get_all(block=True, timeout=timeout)


class FutureFilter:
    """
    This is a filter. First, you populate it with Future
    objects, then you retrieve futures as they are done.
    You can also retrieve futures while feeding the filter.
    The original order of the futures doesn't matter here.

    This class is used by the `as_done` function when its
    `keep_order` option is set to False.
    """

    def __init__(self, futures=None):
        self._futures = list()
        self._lock = threading.RLock()
        self._queue = SimpleQueue()
        self._n = len(self._futures)
        if futures:
            self.populate(futures)

    @property
    def futures(self):
        with self._lock:
            return tuple(self._futures)

    def put(self, future):
        """
        Add a future to the filter

        [param]
        - future: Future object
        """
        with self._lock:
            self._futures.append(future)
            future.add_callback(functools.partial(self._queue.put))
            self._n += 1

    def populate(self, futures):
        """
        Populate the filter

        [param]
        - futures: sequence of Future object
        """
        with self._lock:
            self._futures.extend(futures)
            self._n += len(futures)
        for future in futures:
            future.add_callback(functools.partial(self._queue.put))

    def get(self, block=True, timeout=None):
        """
        Retrieve just one future that is done.

        [param]
        - block: boolean to block until one future is done
        - timeout: None or a timeout value (int or float) in seconds.

        [return]
        Returns a future object that is done
        """
        with self._lock:
            if self._n == 0:
                return
        future = self._get_from_queue(block, timeout)
        return future

    def get_all(self, block=True, timeout=None):
        """
        Yield futures as they are done until the filter is empty

        [param]
        - block: boolean to block until one future is done
        - timeout: None or a timeout value (int or float) in seconds.

        [yield]
        Yield a future object that is done until the filter is empty
        """
        countdown = misc.Countdown(timeout)
        while True:
            with self._lock:
                if self._n == 0:
                    break
            new_timeout = countdown.check()
            future = self._get_from_queue(block, new_timeout)
            yield future

    def _get_from_queue(self, block, timeout):
        try:
            future = self._queue.get(block=block, timeout=timeout)
        except EmptyQueue as e:
            if block:
                raise TimeoutError
            else:
                return
        with self._lock:
            self._n -= 1
        return future


class Future:
    """Future class"""

    def __init__(self, pool, task_id):
        """This class shouldn't be instantiated by the programmer"""
        self._pool = pool
        self._task_id = task_id
        self._on_done_event = threading.Event()
        self._status = None
        self._is_done = False
        self._result = self._duration = self._exception = None
        self._callbacks = list()
        self._mutex = threading.RLock()
        self._pending_duration = self._task_duration = 0
        self._status_to_time = dict()
        self._cancel_flag = False

    @property
    def pool(self):
        return self._pool

    @property
    def task_id(self):
        return self._task_id

    @property
    def is_pending(self):
        with self._mutex:
            return True if self._status == Status.PENDING else False

    @property
    def is_running(self):
        with self._mutex:
            return True if self._status == Status.RUNNING else False

    @property
    def is_completed(self):
        with self._mutex:
            return True if self._status == Status.COMPLETED else False

    @property
    def is_failed(self):
        with self._mutex:
            return True if self._status == Status.FAILED else False

    @property
    def is_cancelled(self):
        with self._mutex:
            return True if self._status == Status.CANCELLED else False

    @property
    def is_done(self):
        with self._mutex:
            return self._is_done

    @property
    def result(self):
        with self._mutex:
            return self._result

    @property
    def duration(self):
        with self._mutex:
            self._update_pending_duration()
            self._update_task_duration()
            return self._pending_duration, self._task_duration

    @property
    def exception(self):
        with self._mutex:
            return self._exception

    @property
    def callbacks(self):
        with self._mutex:
            return tuple(self._callbacks)

    @property
    def cancel_flag(self):
        with self._mutex:
            return self._cancel_flag

    @property
    def status(self):
        with self._mutex:
            return self._status

    def collect(self, timeout=None):
        """
        Collect the result of the task.
        Beware, a remote exception as well as CancelledError,
        or TimeoutError exceptions may be raised.

        [param]
        - timeout: None or a timeout value (int or float) in seconds.

        [return]
        Returns the collected result

        [except]
        - TimeoutError: raised when timeout expires
        - CancelledError: raised when a task got cancelled
        - Exception: any remote exception. Note that the `__context__`
        attribute of a remote exception contains an instance of
        the RemoteError class. The RemoteError class exposes via
        its exc_chain, the exception chain. Applying the builtin
        'str' function on the RemoteError object will return
        the remote traceback as a string.
        """
        r = self._on_done_event.wait(timeout=timeout)
        if r is False:
            raise TimeoutError
        with self._mutex:
            if self._exception is not None:
                raise self._exception
            if self._status == Status.CANCELLED:
                raise errors.CancelledError
            return self._result

    def wait(self, timeout=None):
        """
        Wait (blocking) for the future to be done (completed, failed, or cancelled).

        [param]
        - timeout: None or a timeout value (int or float) in seconds.

        [return]
        Returns True if the future is done in the provided timeout range.
        """
        return self._on_done_event.wait(timeout=timeout)

    def add_callback(self, callback):
        """
        Add one callback that accepts the future as argument.

        [param]
        - callback: the callback to add
        """
        with self._mutex:
            self._callbacks.append(callback)
            if not self._is_done:
                return
            self._execute_callbacks((callback, ))

    def add_callbacks(self, callbacks):
        """
        Add a sequence of callbacks that accept the future as argument.

        [param]
        - callbacks: sequence of callbacks
        """
        with self._mutex:
            self._callbacks.extend(callbacks)
            if not self._is_done:
                return
            self._execute_callbacks(callbacks)

    def remove_callback(self, callback):
        """
        Remove a callback

        [param]
        - callback: the callback to remove
        """
        with self._mutex:
            self._callbacks = [item for item in self._callbacks if item != callback]

    def remove_callbacks(self, callbacks):
        """
        Remove a sequence of callbacks

        [param]
        - callbacks: sequence of callbacks
        """
        with self._mutex:
            self._callbacks = [item for item in self._callbacks if item not in callbacks]

    def cancel(self):
        """
        Tries to cancel the linked task.
        Note that right after, the cancel_flag property is set to True
        and later, the cancelled property will be set to True or not.
        """
        with self._mutex:
            self._cancel_flag = True

    def set_status(self, status, instant=None):
        """Private method ! Don't call it !"""
        instant = time.monotonic() if instant is None else instant
        with self._mutex:
            if self._is_done:
                raise errors.InvalidStateError
            self._status = status
            self._status_to_time[status] = instant
            if status in (Status.COMPLETED, Status.FAILED,
                          Status.CANCELLED):
                self._is_done = True
                self._on_done_event.set()
                self._execute_callbacks(self._callbacks)

    def set_result(self, result, instant=None):
        """Private method ! Don't call it !"""
        instant = time.monotonic() if instant is None else instant
        with self._mutex:
            if self._is_done:
                raise errors.InvalidStateError
            self._result = result
            self.set_status(Status.COMPLETED, instant)

    def set_exception(self, exc, instant=None):
        """Private method ! Don't call it !"""
        instant = time.monotonic() if instant is None else instant
        with self._mutex:
            if self._is_done:
                raise errors.InvalidStateError
            self._exception = exc
            self.set_status(Status.FAILED, instant)

    def _execute_callbacks(self, callbacks):
        for callback in callbacks:
            try:
                callback(self)
            except Exception as e:
                msg = "Exception while calling callback for future {}".format(repr(self))
                misc.LOGGER.exception(msg)

    def _update_pending_duration(self):
        with self._mutex:
            instant_a = self._status_to_time.get(Status.PENDING)
            if not instant_a:
                return
            for status in (Status.COMPLETED, Status.FAILED, Status.CANCELLED):
                instant_b = self._status_to_time.get(status)
                if not instant_b:
                    continue
                self._pending_duration = instant_b - instant_a
                break

    def _update_task_duration(self):
        with self._mutex:
            instant_a = self._status_to_time.get(Status.RUNNING)
            if not instant_a:
                return
            for status in (Status.COMPLETED, Status.FAILED):
                instant_b = self._status_to_time.get(status)
                if not instant_b:
                    continue
                self._task_duration = instant_b - instant_a
                break


@unique
class Status(Enum):
    PENDING = 1
    RUNNING = 2
    COMPLETED = 3
    FAILED = 4
    CANCELLED = 5
