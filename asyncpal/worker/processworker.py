import time
from enum import Enum, unique
from queue import Empty as EmptyQueueError
from asyncpal import errors, misc
from asyncpal.worker import Worker, WorkerType

__all__ = []

@unique
class MessageTag(Enum):
    RUNNING = 1  # tag, task_id
    RESULT = 2  # tag, task_id, result, duration
    EXCEPTION = 3  # tag, task_id, exception
    WORKER_EXCEPTION = 4  # tag, worker_id, exception
    SHUTDOWN = 5  # tag, worker_id


class ProcessWorker(Worker):
    def __init__(self, worker_id, worker_name, task_queue, message_queue,
                 idle_timeout, initializer, init_args, init_kwargs, finalizer,
                 final_args, final_kwargs, max_tasks_per_worker,
                 mp_context):
        super().__init__(WorkerType.PROCESS, worker_id, worker_name,
                         task_queue, idle_timeout, initializer,
                         init_args, init_kwargs, finalizer, final_args,
                         final_kwargs, max_tasks_per_worker)
        self._message_queue = message_queue
        self._mp_context = mp_context
        self._process = None
        self._mutex = self._mp_context.RLock()
        self._is_busy_event = self._mp_context.Event()

    @property
    def message_queue(self):
        return self._message_queue

    @property
    def process(self):
        return self._process

    def run(self):
        with self._mutex:
            if self._process is not None:
                return False
            args = (self._worker_id, self._worker_name, self._task_queue,
                    self._message_queue, self._idle_timeout, self._initializer,
                    self._init_args, self._init_kwargs, self._finalizer,
                    self._final_args, self._final_kwargs,
                    self._max_tasks_per_worker, self._is_busy_event)
            self._process = self._mp_context.Process(name=self._worker_name,
                                                     target=runner, args=args,
                                                     daemon=False)
            self._process.start()
            return True

    def is_alive(self):
        with self._mutex:
            if self._process is None:
                return False
            return self._process.is_alive()

    def is_busy(self):
        return self._is_busy_event.is_set()

    def join(self, timeout=None):
        with self._mutex:
            if self._process is None:
                return False
            self._process.join(timeout=timeout)
            return not self._process.is_alive()


def runner(worker_id, worker_name, task_queue, message_queue, idle_timeout,
           initializer, init_args, init_kwargs,
           finalizer, final_args, final_kwargs,
           max_tasks_per_worker, is_busy_event):
    try:
        if initializer is not None:
            run_initializer(worker_name, initializer, *init_args, **init_kwargs)
        loop(task_queue, message_queue, idle_timeout,
             max_tasks_per_worker, is_busy_event)
        if finalizer is not None:
            run_finalizer(worker_name, finalizer, *final_args, **final_kwargs)
    except BaseException as e:
        misc.LOGGER.critical("Exception in worker", exc_info=True)
        is_busy_event.clear()
        exc = misc.RemoteExceptionWrapper(e)
        e.__traceback__ = e.__cause__ = e.__context__ = None
        msg = (MessageTag.WORKER_EXCEPTION, worker_id, exc)  # WORKER ERROR
        message_queue.put(msg)
    else:
        is_busy_event.clear()
        msg = (MessageTag.SHUTDOWN, worker_id)  # SHUTDOWN
        message_queue.put(msg)


def loop(task_queue, message_queue, idle_timeout,
         max_tasks_per_worker, is_busy_event):
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
        run_task(task, message_queue)
        is_busy_event.clear()
        # task_queue.get might block too long, not giving time to free resource
        # pointed to by 'task', therefore let's free resource as soon as possible
        # by deleting 'task'
        del task
        task_count += 1


def run_task(task, message_queue):
    task_id, target, args, kwargs = task
    # SET RUNNING STATUS
    msg = (MessageTag.RUNNING, task_id, time.monotonic())
    message_queue.put(msg)
    try:
        result = target(*args, **kwargs)
    except BaseException as e:
        # SET EXCEPTION
        exc = misc.RemoteExceptionWrapper(e)
        e.__traceback__ = e.__cause__ = e.__context__ = None
        msg = (MessageTag.EXCEPTION, task_id, exc,
               time.monotonic())
        message_queue.put(msg)
    else:
        # SET RESULT
        msg = (MessageTag.RESULT, task_id, result,
               time.monotonic())
        message_queue.put(msg)


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