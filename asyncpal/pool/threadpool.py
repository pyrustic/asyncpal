"""ThreadPool, SingleThreadPool, DualThreadPool,
TripleThreadPool, and QuadThreadPool are defined here"""
import queue
from asyncpal import misc
from asyncpal.worker.threadworker import ThreadWorker
from asyncpal.pool import Pool, WorkerType, IDLE_TIMEOUT


__all__ = ["ThreadPool", "SingleThreadPool", "DualThreadPool",
           "TripleThreadPool", "QuadThreadPool"]


class ThreadPool(Pool):
    """The ThreadPool class for  preemptive concurrency."""
    def __init__(self, max_workers=None, *, name="ThreadPool",
                 idle_timeout=IDLE_TIMEOUT, initializer=None, init_args=None,
                 init_kwargs=None, finalizer=None, final_args=None,
                 final_kwargs=None, max_tasks_per_worker=None):
        """
        Initialization.

        [param]
        - max_workers: the maximum number of workers. Defaults to CPU count + 5
        - name: the name of the pool. Defaults to the class name
        - idle_timeout: None or a timeout value in seconds.
            The idle timeout tells how much time an inactive worker
            can sleep before it closes. This helps the pool to shrink
            when there isn't much of tasks.
            If you set None, the pool will never shrink. each worker before it closes
        - initializer: a function that will get called at the start of each worker
        - init_args: arguments (list) to pass to the initializer
        - init_kwargs: keyword arguments (dict) to pass to the initializer
        - finalizer: a function that will get called when the worker is going to close
        - final_args: arguments (list) to pass to the finalizer
        - final_kwargs: keyword arguments (dict) to pass to the finalizer
        - max_tasks_per_worker: Maximum number of tasks a worker is allowed to do
            before it closes.
        """
        if max_workers is None or max_workers <= 0:
            x = misc.get_cpu_count() + 5
            max_workers = x if x else 1
        worker_type = WorkerType.THREAD
        task_queue = queue.SimpleQueue()
        super().__init__(worker_type, max_workers=max_workers, name=name,
                         idle_timeout=idle_timeout,
                         initializer=initializer,
                         init_args=init_args, init_kwargs=init_kwargs,
                         finalizer=finalizer, final_args=final_args,
                         final_kwargs=final_kwargs,
                         max_tasks_per_worker=max_tasks_per_worker,
                         task_queue=task_queue)

    def _create_worker(self):
        worker_id = self._monotonic_worker_count
        worker_name = "asyncpal-{}-thread-worker-{}".format(self._name, worker_id)
        with self._vars_lock:
            worker = ThreadWorker(worker_id, worker_name, self._task_queue,
                                  self._idle_timeout, self._initializer,
                                  self._init_args, self._init_kwargs,
                                  self._finalizer, self._final_args,
                                  self._final_kwargs, self._max_tasks_per_worker,
                                  self._on_worker_shutdown, self._on_worker_exception)
            return worker


class SingleThreadPool(ThreadPool):
    """Fixed-size thread pool. This pool can spawn only 1 worker"""
    def __init__(self, *, name="SingleThreadPool", idle_timeout=IDLE_TIMEOUT,
                 initializer=None, init_args=None,
                 init_kwargs=None, finalizer=None, final_args=None,
                 final_kwargs=None, max_tasks_per_worker=None):
        max_workers = 1
        super().__init__(max_workers=max_workers, name=name,
                         idle_timeout=idle_timeout,
                         initializer=initializer,
                         init_args=init_args, init_kwargs=init_kwargs,
                         finalizer=finalizer, final_args=final_args,
                         final_kwargs=final_kwargs,
                         max_tasks_per_worker=max_tasks_per_worker)


class DualThreadPool(ThreadPool):
    """Fixed-size thread pool. This pool can spawn up to 2 workers"""
    def __init__(self, *, name="DualThreadPool", idle_timeout=IDLE_TIMEOUT,
                 initializer=None, init_args=None,
                 init_kwargs=None, finalizer=None, final_args=None,
                 final_kwargs=None, max_tasks_per_worker=None):
        max_workers = 2
        super().__init__(max_workers=max_workers, name=name,
                         idle_timeout=idle_timeout,
                         initializer=initializer,
                         init_args=init_args, init_kwargs=init_kwargs,
                         finalizer=finalizer, final_args=final_args,
                         final_kwargs=final_kwargs,
                         max_tasks_per_worker=max_tasks_per_worker)


class TripleThreadPool(ThreadPool):
    """Fixed-size thread pool. This pool can spawn up to 3 workers"""
    def __init__(self, *, name="TripleThreadPool", idle_timeout=IDLE_TIMEOUT,
                 initializer=None, init_args=None,
                 init_kwargs=None, finalizer=None, final_args=None,
                 final_kwargs=None, max_tasks_per_worker=None):
        max_workers = 3
        super().__init__(max_workers=max_workers, name=name,
                         idle_timeout=idle_timeout,
                         initializer=initializer,
                         init_args=init_args, init_kwargs=init_kwargs,
                         finalizer=finalizer, final_args=final_args,
                         final_kwargs=final_kwargs,
                         max_tasks_per_worker=max_tasks_per_worker)


class QuadThreadPool(ThreadPool):
    """Fixed-size thread pool. This pool can spawn up to 4 workers"""
    def __init__(self, *, name="QuadThreadPool", idle_timeout=IDLE_TIMEOUT,
                 initializer=None, init_args=None,
                 init_kwargs=None, finalizer=None, final_args=None,
                 final_kwargs=None, max_tasks_per_worker=None):
        max_workers = 4
        super().__init__(max_workers=max_workers, name=name,
                         idle_timeout=idle_timeout,
                         initializer=initializer,
                         init_args=init_args, init_kwargs=init_kwargs,
                         finalizer=finalizer, final_args=final_args,
                         final_kwargs=final_kwargs,
                         max_tasks_per_worker=max_tasks_per_worker)
