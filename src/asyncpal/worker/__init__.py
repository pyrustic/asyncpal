from abc import ABC, abstractmethod
from enum import Enum, unique

__all__ = []

@unique
class WorkerType(Enum):
    THREAD = 1
    PROCESS = 2


class Worker(ABC):
    def __init__(self, worker_type, worker_id, worker_name,
                 task_queue, idle_timeout,
                 initializer, init_args, init_kwargs,
                 finalizer, final_args, final_kwargs,
                 max_tasks_per_worker):
        self._worker_type = worker_type
        self._worker_id = worker_id
        self._worker_name = worker_name
        self._task_queue = task_queue
        self._idle_timeout = idle_timeout
        self._initializer = initializer
        self._init_args = init_args
        self._init_kwargs = init_kwargs
        self._finalizer = finalizer
        self._final_args = final_args
        self._final_kwargs = final_kwargs
        self._max_tasks_per_worker = max_tasks_per_worker

    @property
    def worker_type(self):
        return self._worker_type

    @property
    def worker_id(self):
        return self._worker_id

    @property
    def worker_name(self):
        return self._worker_name

    @property
    def task_queue(self):
        return self._task_queue

    @property
    def idle_timeout(self):
        return self._idle_timeout

    @property
    def initializer(self):
        return self._initializer

    @property
    def init_args(self):
        return self._init_args

    @property
    def init_kwargs(self):
        return self._init_kwargs

    @property
    def finalizer(self):
        return self._finalizer

    @property
    def final_args(self):
        return self._final_args

    @property
    def final_kwargs(self):
        return self._final_kwargs

    @property
    def max_tasks_per_worker(self):
        return self._max_tasks_per_worker

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def is_alive(self):
        pass

    @abstractmethod
    def is_busy(self):
        pass

    @abstractmethod
    def join(self, timeout=None):
        pass
