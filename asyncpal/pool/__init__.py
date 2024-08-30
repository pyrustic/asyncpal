"""The abstract base class for all pools is defined here,
as well as the GlobalShutdown class."""
import time
import atexit
import threading
import itertools
import multiprocessing as mp
from abc import ABC, abstractmethod
from collections import deque
from asyncpal import errors
from asyncpal import misc
from asyncpal.future import Future, Status, as_done, FutureFilter
from asyncpal.worker import WorkerType


__all__ = ["Pool", "IDLE_TIMEOUT", "MP_CONTEXT",
           "WINDOWS_MAX_PROCESS_WORKERS"]


IDLE_TIMEOUT = 60
MP_CONTEXT = mp.get_context("spawn")
WINDOWS_MAX_PROCESS_WORKERS = 60


class Pool(ABC):
    def __init__(self, worker_type, max_workers, name,
                 idle_timeout, initializer, init_args,
                 init_kwargs, finalizer, final_args,
                 final_kwargs, max_tasks_per_worker,
                 task_queue, mp_task_queue=None,
                 message_queue=None, mp_context=None):
        # constructor args and kwargs
        self._worker_type = WorkerType(worker_type)
        self._max_workers = max_workers
        self._name = name
        self._idle_timeout = idle_timeout
        self._initializer = initializer
        init_args_kwargs = misc.ensure_args_kwargs(init_args, init_kwargs)
        self._init_args, self._init_kwargs = init_args_kwargs
        final_args_kwargs = misc.ensure_args_kwargs(final_args, final_kwargs)
        self._final_args, self._final_kwargs = final_args_kwargs
        self._finalizer = finalizer
        self._max_tasks_per_worker = max_tasks_per_worker
        self._mp_context = mp_context
        # task queue
        self._task_queue = task_queue
        self._mp_task_queue = mp_task_queue
        # task filter thread
        self._filter_thread = None
        # message queue and message thread for Process based work
        self._message_queue = message_queue
        self._message_thread = None
        # mutexes
        self._vars_lock = self._create_lock()
        self._futures_lock = self._create_lock()
        self._workers_lock = self._create_lock()
        self._pool_lock = self._create_lock()
        #
        self._workers = dict()
        self._inactive_workers = list()
        self._stored_futures = dict()
        self._is_broken = False
        self._cancelled_tasks = list()
        self._is_closed = threading.Event()
        self._is_terminated = False
        self._stored_exception = None
        self._monotonic_worker_count = 0
        self._monotonic_task_count = 0
        self._setup()

    @property
    def worker_type(self):
        return self._worker_type

    @property
    def max_workers(self):
        with self._vars_lock:
            return self._max_workers

    @property
    def name(self):
        return self._name

    @property
    def idle_timeout(self):
        with self._vars_lock:
            return self._idle_timeout

    @idle_timeout.setter
    def idle_timeout(self, val):
        with self._vars_lock:
            self._idle_timeout = val

    @property
    def initializer(self):
        with self._vars_lock:
            return self._initializer

    @property
    def init_args(self):
        with self._vars_lock:
            return self._init_args

    @property
    def init_kwargs(self):
        with self._vars_lock:
            return self._init_kwargs

    @property
    def finalizer(self):
        with self._vars_lock:
            return self._finalizer

    @property
    def final_args(self):
        with self._vars_lock:
            return self._final_args

    @property
    def final_kwargs(self):
        with self._vars_lock:
            return self._final_kwargs

    @property
    def max_tasks_per_worker(self):
        return self._max_tasks_per_worker

    @property
    def mp_context(self):
        return self._mp_context

    @property
    def workers(self):
        with self._vars_lock:
            return tuple(self._workers.values())

    @property
    def cancelled_tasks(self):
        with self._vars_lock:
            return tuple(self._cancelled_tasks)

    @property
    def is_closed(self):
        return self._is_closed.is_set()

    @property
    def is_terminated(self):
        with self._vars_lock:
            return self._is_terminated

    @property
    def is_broken(self):
        with self._vars_lock:
            return self._is_broken

    def check(self):
        """
        Check the pool

        [except]
        - RuntimeError: raised if the pool is closed
        - BrokenPoolError: raised if the pool is broken
        """
        if self._is_closed.is_set():
            raise RuntimeError
        self._ensure_pool_integrity()

    def run(self, target, /, *args, **kwargs):
        """
        Submit the task to the pool, and return
        the result (or re-raise the exception raised by the callable)

        [param]
        - target: callable
        - args: args to pass to the callable
        - kwargs: kwargs to pass to the callable

        [except]
        - RuntimeError: raised when the pool is closed
        - BrokenPoolError: raised when the pool is broken
        - Exception: exception that might be raised by the task itself
        """
        if self._is_closed.is_set():
            raise RuntimeError
        self._ensure_pool_integrity()
        with self._pool_lock:
            return self._submit_task(target, *args, **kwargs).collect()

    def submit(self, target, /, *args, **kwargs):
        """
        Submit the task to the pool, and return
        a future object

        [param]
        - target: callable
        - args: args to pass to the callable
        - kwargs: kwargs to pass to the callable

        [except]
        - RuntimeError: raised when the pool is closed
        - BrokenPoolError: raised when the pool is broken
        - Exception: exception that might be raised by the task itself
        """
        if self._is_closed.is_set():
            raise RuntimeError
        self._ensure_pool_integrity()
        with self._pool_lock:
            return self._submit_task(target, *args, **kwargs)

    def map(self, target, *iterables, chunk_size=1, buffer_size=1,
            keep_order=True, timeout=None):
        """
        Perform a Map operation lazily and return an iterator
        that iterates over the results.
        Beware, a remote exception will be reraised here

        [param]
        - target: callable
        - iterables: iterables to pass to the target
        - chunk_size: max length for a chunk
        - buffer_size: the buffer_size. A bigger size will consume more memory
            but the overall operation will be faster
        - keep_order: whether the original order should be kept or not
        - timeout: None or a timeout (int or float) value in seconds

        [return]
        Returns an iterator

        [except]
        - RuntimeError: raised when the pool is closed
        - BrokenPoolError: raised when the pool is broken
        - Exception: any remote exception
        """
        if self._is_closed.is_set():
            raise RuntimeError
        self._ensure_pool_integrity()
        with self._pool_lock:
            if chunk_size == 1 and keep_order:
                return self._map_lazy(target, zip(*iterables),
                                      buffer_size=buffer_size,
                                      timeout=timeout)
            elif chunk_size == 1:
                return self._map_lazy_unordered(target, zip(*iterables),
                                                buffer_size=buffer_size,
                                                timeout=timeout)
            elif keep_order:
                return self._map_lazy_chunked(target, zip(*iterables),
                                              chunk_size=chunk_size,
                                              buffer_size=buffer_size,
                                              timeout=timeout)
            else:
                return self._map_lazy_chunked_unordered(target, zip(*iterables),
                                                        chunk_size=chunk_size,
                                                        buffer_size=buffer_size,
                                                        timeout=timeout)

    def map_unordered(self, target, *iterables,
                      chunk_size=1, buffer_size=1,
                      timeout=None):
        """Same as map with 'keep_order' set to False"""
        return self.map(target, *iterables, chunk_size=chunk_size,
                        buffer_size=buffer_size, keep_order=False,
                        timeout=timeout)

    def map_all(self, target, *iterables, chunk_size=1,
                keep_order=True, timeout=None):
        """
        Perform a Map operation eagerly and return an iterator
        that iterates over the results.
        Using this method instead of the `map` method might cause high memory usage.
        Beware, a remote exception will be reraised here

        [param]
        - target: callable
        - iterables: iterables to pass to the target
        - chunk_size: max length for a chunk
        - keep_order: whether the original order should be kept or not
        - timeout: None or a timeout (int or float) value in seconds

        [return]
        Returns an iterator that iterates over the results.

        [except]
        - RuntimeError: raised when the pool is closed
        - BrokenPoolError: raised when the pool is broken
        - Exception: any remote exception
        """
        if self._is_closed.is_set():
            raise RuntimeError
        self._ensure_pool_integrity()
        with self._pool_lock:
            if chunk_size == 1:
                return self._map_eager(target, zip(*iterables),
                                       keep_order=keep_order,
                                       timeout=timeout)
            else:
                return self._map_eager_chunked(target, zip(*iterables),
                                               chunk_size=chunk_size,
                                               keep_order=keep_order,
                                               timeout=timeout)

    def map_all_unordered(self, target, *iterables, chunk_size=1,
                         timeout=None):
        """Same as map with 'keep_order' set to False"""
        return self.map_all(target, *iterables, chunk_size=chunk_size,
                            keep_order=False, timeout=timeout)

    def starmap(self, target, iterable, chunk_size=1, buffer_size=1,
                keep_order=True, timeout=None):
        """
        Perform a Starmap operation lazily and return an iterator
        that iterates over the results.
        Beware, a remote exception will be reraised here

        [param]
        - target: callable
        - iterable: sequence of args to pass to the target
        - chunk_size: max length for a chunk
        - buffer_size: the buffer_size. A bigger size will consume more memory
            but the overall operation will be faster
        - keep_order: whether the original order should be kept or not
        - timeout: None or a timeout (int or float) value in seconds

        [return]
        Returns an iterator that iterates over the results.

        [except]
        - RuntimeError: raised when the pool is closed
        - BrokenPoolError: raised when the pool is broken
        - Exception: any remote exception
        """
        if self._is_closed.is_set():
            raise RuntimeError
        self._ensure_pool_integrity()
        with self._pool_lock:
            if chunk_size == 1 and keep_order:
                return self._map_lazy(target, iterable,
                                      buffer_size=buffer_size,
                                      timeout=timeout)
            elif chunk_size == 1:
                return self._map_lazy_unordered(target, iterable,
                                                buffer_size=buffer_size,
                                                timeout=timeout)
            elif keep_order:
                return self._map_lazy_chunked(target, iterable,
                                              chunk_size=chunk_size,
                                              buffer_size=buffer_size,
                                              timeout=timeout)
            else:
                return self._map_lazy_chunked_unordered(target, iterable,
                                                        chunk_size=chunk_size,
                                                        buffer_size=buffer_size,
                                                        timeout=timeout)

    def starmap_unordered(self, target, iterable, chunk_size=1,
                          buffer_size=1, timeout=None):
        """Same as starmap with 'keep_order' set to False"""
        return self.starmap(target, iterable, chunk_size=chunk_size,
                            buffer_size=buffer_size, keep_order=False,
                            timeout=timeout)

    def starmap_all(self, target, iterable, chunk_size=1,
                    keep_order=True, timeout=None):
        """
        Perform a Starmap operation eagerly and return an iterator
        that iterates over the results.
        Using this method instead of the `map` method might cause high memory usage.
        Beware, a remote exception will be reraised here

        [param]
        - target: callable
        - iterable: sequence of args to pass to the target
        - chunk_size: max length for a chunk
        - keep_order: whether the original order should be kept or not
        - timeout: None or a timeout (int or float) value in seconds

        [return]
        Returns an iterator that iterates over the results.

        [except]
        - RuntimeError: raised when the pool is closed
        - BrokenPoolError: raised when the pool is broken
        - Exception: any remote exception
        """
        if self._is_closed.is_set():
            raise RuntimeError
        self._ensure_pool_integrity()
        with self._pool_lock:
            if chunk_size == 1:
                return self._map_eager(target, iterable,
                                       keep_order=keep_order,
                                       timeout=timeout)
            else:
                return self._map_eager_chunked(target, iterable,
                                               chunk_size=chunk_size,
                                               keep_order=keep_order,
                                               timeout=timeout)

    def starmap_all_unordered(self, target, iterable, chunk_size=1,
                              timeout=None):
        """Same as starmap_all with 'keep_order' set to False"""
        return self.starmap_all(target, iterable, chunk_size=chunk_size,
                                keep_order=False, timeout=timeout)

    def test(self):
        """Test the pool by creating another pool with the same config
        and doing some computation on it to ensure that it won't break.
        This method might raise a BrokenPoolError exception
        """
        if self._is_closed.is_set():
            raise RuntimeError
        self._ensure_pool_integrity()
        kwargs = {"max_workers": 1,
                  "idle_timeout": self._idle_timeout,
                  "initializer": self._initializer,
                  "init_args": self._init_args,
                  "init_kwargs": self._init_kwargs,
                  "finalizer": self._finalizer,
                  "final_args": self._final_args,
                  "final_kwargs": self._final_kwargs,
                  "max_tasks_per_worker": self._max_tasks_per_worker}
        pool_class = self.__class__
        if self._worker_type == WorkerType.THREAD:
            name = "test_threadpool_" + str(int(time.time()))
        else:
            name = "test_processpool_" + str(int(time.time()))
            kwargs["mp_context"] = self._mp_context
        kwargs["name"] = name
        with pool_class(**kwargs) as pool:
            it = range(10)
            # with .submit
            r = pool.submit(misc.add, 1, 2).collect()
            assert r == 3
            # with .map
            r = tuple(pool.map(misc.add, it, it, chunk_size=2))
            assert r == tuple(map(misc.add, it, it))
            # with .starmap
            r = tuple(pool.starmap(misc.add, zip(it, it), chunk_size=2))
            assert r == tuple(itertools.starmap(misc.add, zip(it, it)))
            # check !
            pool.check()

    def spawn_workers(self, n=None):
        """Spawn a specific number of workers or the right number
        of workers that is needed

        [param]
        - n: None or an integer.

        [return]
        Returns the number of spawned workers
        """
        if self._is_closed.is_set():
            raise RuntimeError
        self._ensure_pool_integrity()
        with self._pool_lock:
            return self._spawn_workers(n)

    def spawn_max_workers(self):
        """Spawn the maximum number of workers"""
        if self._is_closed.is_set():
            raise RuntimeError
        self._ensure_pool_integrity()
        with self._pool_lock:
            self._spawn_workers(self._max_workers)

    def count_workers(self):
        """Returns the number of workers that are alive"""
        if self._is_closed.is_set():
            return 0
        with self._pool_lock:
            return self._count_workers()

    def count_busy_workers(self):
        """Returns the number of busy workers"""
        if self._is_closed.is_set():
            return 0
        with self._pool_lock:
            return self._count_busy_workers()

    def count_free_workers(self):
        """Returns the number of free workers"""
        if self._is_closed.is_set():
            return 0
        with self._pool_lock:
            return self._count_free_workers()

    def count_pending_tasks(self):
        """Returns the number of pending tasks"""
        if self._is_closed.is_set():
            return 0
        with self._pool_lock:
            return self._count_pending_tasks()

    def join(self, timeout=None):
        """
        Join the workers, i.e., wait for workers to end their works, then close them

        [param]
        - timeout: None or a number representing seconds.

        [except]
        - RuntimeError: raised when timeout expires
        """
        if self._is_closed.is_set():
            return False
        self._is_closed.set()
        with self._pool_lock:
            self._notify_workers_to_shutdown()
            r = self._join_workers(timeout)
        self._is_closed.clear()
        return r

    def shutdown(self):
        """
        Close the pool by joining workers and cancelling pending tasks.
        Note that cancelled tasks can be retrieved via the cancelled_tasks property.

        [return]
        Returns False if the pool has already been closed, else returns True.
        """
        if self._is_closed.is_set():
            return False
        with self._pool_lock:
            self._is_closed.set()
            self._cancel_tasks()
            self._notify_workers_to_shutdown()
            self._join_workers()
            self._cleanup_task_queue()
            if self._worker_type == WorkerType.PROCESS:
                self._shutdown_filter_thread()
                self._shutdown_message_thread()
            self._cleanup_stored_futures()
            self._workers = dict()
            self._is_terminated = True
            self._stored_exception = None
            GlobalShutdown.deregister(self.shutdown)
            return True

    def _setup(self):
        GlobalShutdown.register(self.shutdown)
        GlobalShutdown.activate()

    def _spawn_filter_thread(self):
        thread_name = "asyncpal-{}-FilterThread".format(self._name)
        self._filter_thread = threading.Thread(name=thread_name,
                                               target=self._filter_tasks,
                                               daemon=False)
        self._filter_thread.start()

    def _spawn_workers(self, n=None):
        if n is None:
            n_workers = self._count_workers()
            n_free_workers = self._count_free_workers()
            n_tasks = self._count_pending_tasks()
            max_n = self._max_workers - n_workers
            n = max(0, min(max_n, n_tasks - n_free_workers))
        with self._workers_lock:
            for _ in range(n):
                self._monotonic_worker_count += 1
                worker = self._create_worker()
                self._workers[worker.worker_id] = worker
                worker.run()
        return n

    def _create_lock(self):
        return (threading.RLock()
                if self._worker_type == WorkerType.THREAD
                else self._mp_context.RLock())

    def _count_workers(self):
        with self._workers_lock:
            i = 0
            for worker in self._workers.values():
                if worker.is_alive():
                    i += 1
            return i

    def _count_busy_workers(self):
        with self._workers_lock:
            i = 0
            for worker in self._workers.values():
                if worker.is_busy():
                    i += 1
            return i

    def _count_free_workers(self):
        with self._workers_lock:
            i = 0
            for worker in self._workers.values():
                if not worker.is_busy():
                    i += 1
            return i

    def _count_pending_tasks(self):
        n = self._task_queue.qsize()
        if self._worker_type == WorkerType.PROCESS:
            n += self._mp_task_queue.qsize()
        return n

    def _ensure_pool_integrity(self):
        with self._vars_lock:
            if self._stored_exception is None:
                return
            if isinstance(self._stored_exception, errors.BrokenPoolError):
                raise self._stored_exception
            else:
                raise errors.BrokenPoolError from self._stored_exception

    @abstractmethod
    def _create_worker(self):
        pass

    def _submit_task(self, target, *args, **kwargs):
        self._join_inactive_workers()
        self._monotonic_task_count += 1
        task_id = self._monotonic_task_count
        future = Future(self, task_id)
        future.set_status(Status.PENDING)
        if self._worker_type == WorkerType.PROCESS:
            with self._futures_lock:
                self._stored_futures[task_id] = future
        task = (future, target, args, kwargs)
        self._task_queue.put(task)
        # ensure workers
        self._spawn_workers()
        return future

    def _map_lazy(self, target, iterable, buffer_size, timeout):
        countdown = misc.Countdown(timeout)
        buffer = deque()
        for i, args in enumerate(iterable):
            future = self._submit_task(target, *args)
            buffer.append(future)
            if i >= buffer_size - 1:
                future = buffer.popleft()
                new_timeout = countdown.check()
                yield future.collect(new_timeout)
        # consume buffer
        for future in buffer:
            new_timeout = countdown.check()
            yield future.collect(new_timeout)

    def _map_lazy_unordered(self, target, iterable, buffer_size, timeout):
        countdown = misc.Countdown(timeout)
        future_filter = FutureFilter()
        for i, args in enumerate(iterable):
            future = self._submit_task(target, *args)
            future_filter.put(future)
            if i >= buffer_size - 1:
                new_timeout = countdown.check()
                future = future_filter.get(timeout=new_timeout)
                yield future.collect()
        new_timeout = countdown.check()
        for future in future_filter.get_all(timeout=new_timeout):
            yield future.collect()

    def _map_lazy_chunked(self, target, iterable, chunk_size,
                          buffer_size, timeout):
        countdown = misc.Countdown(timeout)
        buffer = deque()
        for i, subtask in enumerate(misc.split_starmap_task(target,
                                                            iterable,
                                                            chunk_size=chunk_size)):
            future = self._submit_task(subtask)
            buffer.append(future)
            if i >= buffer_size - 1:
                future = buffer.popleft()
                new_timeout = countdown.check()
                for value in future.collect(new_timeout):
                    yield value
        # consume buffer
        for future in buffer:
            new_timeout = countdown.check()
            for value in future.collect(new_timeout):
                yield value

    def _map_lazy_chunked_unordered(self, target, iterable, chunk_size,
                                    buffer_size, timeout):
        countdown = misc.Countdown(timeout)
        future_filter = FutureFilter()
        for i, subtask in enumerate(misc.split_starmap_task(target,
                                                            iterable,
                                                            chunk_size=chunk_size)):
            future = self._submit_task(subtask)
            future_filter.put(future)
            if i >= buffer_size - 1:
                new_timeout = countdown.check()
                future = future_filter.get(timeout=new_timeout)
                for value in future.collect():
                    yield value
        new_timeout = countdown.check()
        for future in future_filter.get_all(timeout=new_timeout):
            for value in future.collect():
                yield value

    def _map_eager(self, target, iterable, keep_order, timeout):
        futures = [self._submit_task(target, *args) for args in iterable]
        return _collect_results(futures, keep_order=keep_order, timeout=timeout)

    def _map_eager_chunked(self, target, iterable, chunk_size,
                           keep_order, timeout):
        futures = list()
        for subtask in misc.split_starmap_task(target, iterable,
                                               chunk_size=chunk_size):
            future = self._submit_task(subtask)
            futures.append(future)
        return _collect_batched_results(futures, timeout=timeout,
                                        keep_order=keep_order)

    def _filter_tasks(self):
        while True:
            task = self._task_queue.get(block=True, timeout=None)
            if task is None:
                break
            future, target, args, kwargs = task
            if future.cancel_flag:
                future.set_status(Status.CANCELLED)
                with self._futures_lock:
                    del self._stored_futures[future.task_id]
                continue
            task = (future.task_id, target, args, kwargs)
            self._mp_task_queue.put(task, block=True, timeout=None)
            # delete references to objects as they might be holden
            # for too long because self._tasks_queue.get is a blocking call
            del task, future, target, args, kwargs

    def _on_worker_shutdown(self, worker_id):
        with self._workers_lock:
            try:
                worker = self._workers[worker_id]
            except KeyError as e:
                pass
            else:
                self._inactive_workers.append(worker)
                del self._workers[worker_id]
        if not self._is_closed.is_set():
            self._spawn_workers()

    def _on_worker_exception(self, worker_id, exc):
        with self._workers_lock:
            try:
                worker = self._workers[worker_id]
            except KeyError as e:
                pass
            else:
                self._inactive_workers.append(worker)
                del self._workers[worker_id]
        with self._vars_lock:
            if self._stored_exception is None:
                self._cancel_tasks()
                self._notify_workers_to_shutdown()
            self._stored_exception = exc
            self._is_broken = True

    def _notify_workers_to_shutdown(self):
        n = self._count_workers()
        task_queue = (self._task_queue
                      if self._worker_type == WorkerType.THREAD
                      else self._mp_task_queue)
        for _ in range(n):
            task_queue.put(None)

    def _cancel_tasks(self):  # called only once on shutdown !
        # drain the task queue and cancel futures
        tasks, futures = self._drain_task_queue()
        # drain the mp_task queue and cancel futures
        if self._worker_type == WorkerType.PROCESS:
            t, f = self._drain_mp_task_queue()
            tasks.extend(t)
            futures.extend(f)
        self._cancelled_tasks.extend(tasks)
        with self._futures_lock:
            for future in futures:
                future.set_status(Status.CANCELLED)
                try:
                    del self._stored_futures[future.task_id]
                except KeyError as e:
                    pass

    def _drain_task_queue(self):
        tasks = list()
        futures = list()
        # drain the task queue and cancel futures
        for task in misc.iterate_queue(self._task_queue):
            if task is None:
                continue
            future, target, args, kwargs = task
            futures.append(future)
            tasks.append((target, args, kwargs))
        return tasks, futures

    def _drain_mp_task_queue(self):
        tasks = list()
        task_ids = list()
        futures = list()
        for task in misc.iterate_queue(self._mp_task_queue):
            if task is None:
                continue
            task_id, target, args, kwargs = task
            task_ids.append(task_id)
            tasks.append((target, args, kwargs))
        with self._futures_lock:
            for task_id in task_ids:
                try:
                    future = self._stored_futures[task_id]
                except KeyError as e:
                    pass
                else:
                    futures.append(future)
        return tasks, futures

    def _join_inactive_workers(self):
        with self._workers_lock:
            for worker in self._inactive_workers:
                worker.join()
            self._inactive_workers = list()

    def _join_workers(self, timeout=None):
        with self._workers_lock:
            workers = tuple(self._workers.values())
        countdown = misc.Countdown(timeout)
        for worker in workers:
            if timeout is None:
                new_timeout = None
            else:
                new_timeout = countdown.check()
            if not worker.join(new_timeout):
                return False
        return True

    def _shutdown_message_thread(self):
        self._message_queue.put(None)
        self._message_thread.join()
        self._message_thread = None

    def _shutdown_filter_thread(self):
        self._task_queue.put(None)
        self._filter_thread.join()

    def _cleanup_task_queue(self):
        misc.drain_queue(self._task_queue)
        if self._worker_type == WorkerType.PROCESS:
            # spurious BrokenPipeError might happen while
            # trying to close the queue. A 1ms sleep fixes it !
            # See: https://github.com/python/cpython/issues/91185
            # See also: https://github.com/python/cpython/pull/31913
            time.sleep(0.001)
            # mp task queue is a multiprocessing Queue,
            # therefore to join it: .close() then .join_thread()
            self._mp_task_queue.close()
            self._mp_task_queue.join_thread()

    def _cleanup_stored_futures(self):
        with self._futures_lock:
            futures = self._stored_futures.values()
            self._stored_futures = dict()
        for future in futures:
            future.set_status(Status.CANCELLED)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()

    def __del__(self):
        self.shutdown()


def _collect_batched_results(futures, keep_order=True, timeout=None):
    for future in as_done(futures, keep_order=keep_order, timeout=timeout):
        for value in future.collect():
            yield value


def _collect_results(futures, keep_order=True, timeout=None):
    for future in as_done(futures, keep_order=keep_order, timeout=timeout):
        yield future.collect()


class GlobalShutdown:
    """Workaround to be able to use daemon threads and still gracefully shut down
    the pools at exit without having to use the atexit function"""
    _lock = threading.Lock()
    _handlers = list()
    _thread = None

    @classmethod
    def activate(cls):
        with cls._lock:
            if cls._thread is None:
                cls._thread = threading.Thread(target=global_shutdown_runner,
                                               daemon=False)
                cls._thread.start()

    @classmethod
    def is_active(cls):
        with cls._lock:
            return False if cls._thread is None else True

    @classmethod
    def join_thread(cls):
        """Join the globalshutdown thread"""
        with cls._lock:
            if cls._thread is not None:
                cls._thread.join()

    @classmethod
    def register(cls, handler):
        """Register a pool shutdown handler"""
        with cls._lock:
            cls._handlers.append(handler)

    @classmethod
    def deregister(cls, handler):
        """
        https://github.com/AxonFramework/AxonFramework/issues/2456
        https://english.stackexchange.com/questions/25931/unregister-vs-deregister
        """
        with cls._lock:
            cls._handlers = [h for h in cls._handlers if h != handler]

    @classmethod
    def count_handlers(cls):
        with cls._lock:
            return len(cls._handlers)

    @classmethod
    def get_handlers(cls):
        with cls._lock:
            return tuple(cls._handlers)


def global_shutdown_runner():
    """Join the main thread then run the shutdown handlers registered by pools.
    Note that the main thread can only be joined when it stops."""
    threading.main_thread().join(timeout=None)
    for handler in GlobalShutdown.get_handlers():
        handler()


atexit.register(GlobalShutdown.join_thread)
GlobalShutdown.activate()
