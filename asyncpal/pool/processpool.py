"""ProcessPool, SingleProcessPool, DualProcessPool,
TripleProcessPool, and QuadProcessPool are defined here"""
import sys
import threading
import queue
from asyncpal import errors
from asyncpal import misc
from asyncpal.future import Status
from asyncpal.worker.processworker import ProcessWorker, MessageTag
from asyncpal.pool import Pool, WorkerType, IDLE_TIMEOUT, MP_CONTEXT, WINDOWS_MAX_PROCESS_WORKERS


__all__ = ["ProcessPool", "SingleProcessPool", "DualProcessPool",
           "TripleProcessPool", "QuadProcessPool"]


class ProcessPool(Pool):
    """The ProcessPool class for parallelism."""
    def __init__(self, max_workers=None, *, name="ProcessPool",
                 idle_timeout=IDLE_TIMEOUT, initializer=None, init_args=None,
                 init_kwargs=None, finalizer=None, final_args=None,
                 final_kwargs=None, max_tasks_per_worker=None, mp_context=None):
        """
        Initialization.

        [param]
        - max_workers: the maximum number of workers. Defaults to CPU count. On Windows,
            the maximum number that is accepted for the max_workers is 60.
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
        - mp_context: the multiprocessing context.
            Defaults to multiprocessing.get_context("spawn")
        """
        if max_workers:
            if sys.platform == "win32" and max_workers > WINDOWS_MAX_PROCESS_WORKERS:
                msg = "Max process workers on Windows is {}".format(WINDOWS_MAX_PROCESS_WORKERS)
                raise ValueError(msg)
        else:
            x = misc.get_cpu_count()
            max_workers = x if x else 1
        worker_type = WorkerType.PROCESS
        mp_context = MP_CONTEXT if mp_context is None else mp_context
        task_queue = queue.SimpleQueue()
        mp_task_queue = mp_context.Queue(maxsize=max_workers+1)
        message_queue = mp_context.SimpleQueue()
        super().__init__(worker_type, max_workers=max_workers, name=name,
                         idle_timeout=idle_timeout,
                         initializer=initializer, init_args=init_args,
                         init_kwargs=init_kwargs, finalizer=finalizer,
                         final_args=final_args, final_kwargs=final_kwargs,
                         max_tasks_per_worker=max_tasks_per_worker,
                         task_queue=task_queue, mp_task_queue=mp_task_queue,
                         message_queue=message_queue, mp_context=mp_context)
        self._spawn_filter_thread()
        self._spawn_message_thread()

    def _create_worker(self):
        worker_id = self._monotonic_worker_count
        worker_name = "asyncpal-{}-process-worker-{}".format(self._name, worker_id)
        with self._vars_lock:
            worker = ProcessWorker(worker_id, worker_name, self._mp_task_queue,
                                   self._message_queue,
                                   self._idle_timeout, self._initializer,
                                   self._init_args, self._init_kwargs,
                                   self._finalizer, self._final_args,
                                   self._final_kwargs,
                                   self._max_tasks_per_worker,
                                   self._mp_context)
            return worker

    def _spawn_message_thread(self):
        thread_name = "asyncpal-{}-MessageThread".format(self._name)
        self._message_thread = threading.Thread(name=thread_name,
                                                target=self._consume_message_queue,
                                                daemon=False)
        self._message_thread.start()

    def _consume_message_queue(self):
        # special loop working inside a thread to support
        # Process Workers by consuming/dispatching the messages
        # they put in the message_queue
        while True:
            message = self._message_queue.get()
            if message is None:
                break
            try:
                tag = message[0]
                if tag in (MessageTag.RUNNING, MessageTag.RESULT,
                           MessageTag.EXCEPTION):
                    self._update_future(message)
                elif tag == MessageTag.SHUTDOWN:
                    self._on_worker_shutdown(message[1])
                elif tag == MessageTag.WORKER_EXCEPTION:
                    worker_id, exc_wrapper = message[1:]
                    exc = exc_wrapper.unwrap()
                    self._on_worker_exception(worker_id, exc)
                else:
                    msg = "Invalid message tag: {}".format(tag)
                    e = errors.Error(msg)
                    raise e
            except BaseException as e:
                with self._vars_lock:
                    self._stored_exception = e
                raise e
            # message_queue.get might block too long, not giving time to free resource
            # pointed to by 'message', therefore let's free resource as soon as possible
            # by deleting 'message'
            del message

    def _update_future(self, message):
        # this method is solely called by the message_thread
        # that works only for Process Workers to dispatch results/notifs
        tag, task_id = message[0:2]
        with self._futures_lock:
            future = self._stored_futures[task_id]
        if tag == MessageTag.RUNNING:
            instant = message[2]
            future.set_status(Status.RUNNING, instant)
        elif tag == MessageTag.RESULT:
            result, instant = message[2:]
            future.set_result(result, instant)
        elif tag == MessageTag.EXCEPTION:
            exc_wrapper, instant = message[2:]
            exc = exc_wrapper.unwrap()
            future.set_exception(exc, instant)
        if tag in (MessageTag.RESULT, MessageTag.EXCEPTION):
            with self._futures_lock:
                del self._stored_futures[task_id]

    def __reduce__(self):
        msg = "A pool object cannot be pickled"
        raise NotImplementedError(msg)


class SingleProcessPool(ProcessPool):
    """Fixed-size process pool. This pool can spawn only 1 worker"""
    def __init__(self, *, name="SingleProcessPool",
                 idle_timeout=IDLE_TIMEOUT, initializer=None, init_args=None,
                 init_kwargs=None, finalizer=None, final_args=None,
                 final_kwargs=None, max_tasks_per_worker=None, mp_context=None):
        max_workers = 1
        super().__init__(max_workers=max_workers, name=name,
                         idle_timeout=idle_timeout,
                         initializer=initializer, init_args=init_args,
                         init_kwargs=init_kwargs, finalizer=finalizer,
                         final_args=final_args, final_kwargs=final_kwargs,
                         max_tasks_per_worker=max_tasks_per_worker,
                         mp_context=mp_context)


class DualProcessPool(ProcessPool):
    """Fixed-size process pool. This pool can spawn up to 2 workers"""
    def __init__(self, *, name="DualProcessPool",
                 idle_timeout=IDLE_TIMEOUT, initializer=None, init_args=None,
                 init_kwargs=None, finalizer=None, final_args=None,
                 final_kwargs=None, max_tasks_per_worker=None, mp_context=None):
        max_workers = 2
        super().__init__(max_workers=max_workers, name=name,
                         idle_timeout=idle_timeout,
                         initializer=initializer, init_args=init_args,
                         init_kwargs=init_kwargs, finalizer=finalizer,
                         final_args=final_args, final_kwargs=final_kwargs,
                         max_tasks_per_worker=max_tasks_per_worker,
                         mp_context=mp_context)


class TripleProcessPool(ProcessPool):
    """Fixed-size process pool. This pool can spawn up to 3 workers"""
    def __init__(self, *, name="TripleProcessPool",
                 idle_timeout=IDLE_TIMEOUT, initializer=None, init_args=None,
                 init_kwargs=None, finalizer=None, final_args=None,
                 final_kwargs=None, max_tasks_per_worker=None, mp_context=None):
        max_workers = 3
        super().__init__(max_workers=max_workers, name=name,
                         idle_timeout=idle_timeout,
                         initializer=initializer, init_args=init_args,
                         init_kwargs=init_kwargs, finalizer=finalizer,
                         final_args=final_args, final_kwargs=final_kwargs,
                         max_tasks_per_worker=max_tasks_per_worker,
                         mp_context=mp_context)


class QuadProcessPool(ProcessPool):
    """Fixed-size process pool. This pool can spawn up to 4 workers"""
    def __init__(self, *, name="QuadProcessPool",
                 idle_timeout=IDLE_TIMEOUT, initializer=None, init_args=None,
                 init_kwargs=None, finalizer=None, final_args=None,
                 final_kwargs=None, max_tasks_per_worker=None, mp_context=None):
        max_workers = 4
        super().__init__(max_workers=max_workers, name=name,
                         idle_timeout=idle_timeout,
                         initializer=initializer, init_args=init_args,
                         init_kwargs=init_kwargs, finalizer=finalizer,
                         final_args=final_args, final_kwargs=final_kwargs,
                         max_tasks_per_worker=max_tasks_per_worker,
                         mp_context=mp_context)
