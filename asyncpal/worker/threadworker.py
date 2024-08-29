import time
import threading
from queue import Empty as EmptyQueueError
from asyncpal import errors, misc
from asyncpal.future import Status
from asyncpal.worker import Worker, WorkerType

__all__ = []

class ThreadWorker(Worker):
    def __init__(self, worker_id, worker_name, task_queue, idle_timeout, initializer,
                 init_args, init_kwargs, finalizer, final_args, final_kwargs,
                 max_tasks_per_worker, on_shutdown, on_exception):
        super().__init__(WorkerType.THREAD, worker_id, worker_name,
                         task_queue, idle_timeout, initializer,
                         init_args, init_kwargs, finalizer, final_args, final_kwargs,
                         max_tasks_per_worker)
        self._on_shutdown = on_shutdown
        self._on_exception = on_exception
        self._thread = None
        self._mutex = threading.RLock()
        self._is_busy_event = threading.Event()

    @property
    def thread(self):
        return self._thread

    @property
    def on_shutdown(self):
        return self._on_shutdown

    @property
    def on_exception(self):
        return self._on_exception

    def run(self):
        with self._mutex:
            if self._thread is not None:
                return False
            args = (self._worker_id, self._worker_name, self._task_queue, self._idle_timeout,
                    self._initializer, self._init_args, self._init_kwargs,
                    self._finalizer, self._final_args, self._final_kwargs,
                    self._max_tasks_per_worker, self._is_busy_event,
                    self._on_shutdown, self._on_exception)
            self._thread = threading.Thread(name=self._worker_name, target=runner,
                                            args=args, daemon=False)
            self._thread.start()
            return True

    def is_alive(self):
        with self._mutex:
            if self._thread is None:
                return False
            return self._thread.is_alive()

    def is_busy(self):
        return self._is_busy_event.is_set()

    def join(self, timeout=None):
        with self._mutex:
            if self._thread is None:
                return False
            self._thread.join(timeout=timeout)
            return not self._thread.is_alive()


def runner(worker_id, worker_name, task_queue, idle_timeout,
           initializer, init_args, init_kwargs,
           finalizer, final_args, final_kwargs,
           max_tasks_per_worker, is_busy_event,
           on_shutdown, on_exception):
    try:
        if initializer is not None:
            run_initializer(worker_name, initializer, *init_args, **init_kwargs)
        loop(task_queue, idle_timeout, max_tasks_per_worker, is_busy_event)
        if finalizer is not None:
            run_finalizer(worker_name, finalizer, *final_args, **final_kwargs)
    except BaseException as e:
        misc.LOGGER.critical("Exception in worker", exc_info=True)
        is_busy_event.clear()
        on_exception(worker_id, e)
    else:
        is_busy_event.clear()
        on_shutdown(worker_id)


def loop(task_queue, idle_timeout, max_tasks_per_worker, is_busy_event):
    task_count = 0
    while True:
        if max_tasks_per_worker and max_tasks_per_worker == task_count:
            break
        try:
            task = task_queue.get(block=True, timeout=idle_timeout)
        except EmptyQueueError as e:
            break
        if task is None:
            break
        is_busy_event.set()
        run_task(task)
        is_busy_event.clear()
        # task_queue.get might block too long, not giving time to free resource
        # pointed to by 'task', therefore let's free resource as soon as possible
        # by deleting 'task'
        del task
        task_count += 1


def run_task(task):
    future, target, args, kwargs = task
    # SET RUNNING STATUS
    future.set_status(Status.RUNNING, time.monotonic())
    if future.cancel_flag:
        future.set_status(Status.CANCELLED)
        return
    try:
        result = target(*args, **kwargs)
    except BaseException as e:
        # SET EXCEPTION
        future.set_exception(e, time.monotonic())
    else:
        # SET RESULT
        future.set_result(result, time.monotonic())


def run_initializer(worker_name, initializer, *init_args, **init_kwargs):
    try:
        initializer(*init_args, **init_kwargs)
    except BaseException as e:
        msg = "Initialization error in '{}'.".format(worker_name)
        raise errors.InitializerError(msg) from e


def run_finalizer(worker_name, finalizer, *final_args, **final_kwargs):
    try:
        finalizer(*final_args, **final_kwargs)
    except BaseException as e:
        msg = "Finalization error in '{}'.".format(worker_name)
        raise errors.FinalizerError(msg) from e
