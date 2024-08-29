###### Asyncpal API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/asyncpal/__init__/README.md) | [Source](/asyncpal/__init__.py)

# Class DualThreadPool
> Module: [asyncpal.\_\_init\_\_](/docs/api/modules/asyncpal/__init__/README.md)
>
> Class: **DualThreadPool**
>
> Inheritance: [asyncpal.pool.threadpool.ThreadPool](/docs/api/modules/asyncpal/pool/threadpool/class-ThreadPool.md)

Fixed-size thread pool. This pool can spawn up to 2 workers

## Fields table
Here are fields exposed in the class:

| Field | Value |
| --- | --- |
| \_abc\_impl | `<_abc_data object at 0x7f8d031ce990>` |

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## Properties table
Here are properties exposed in the class:

| Property | Methods | Description |
| --- | --- | --- |
| broken | _getter_ | No docstring. |
| cancelled\_tasks | _getter_ | No docstring. |
| closed | _getter_ | No docstring. |
| final\_args | _getter_ | No docstring. |
| final\_kwargs | _getter_ | No docstring. |
| finalizer | _getter_ | No docstring. |
| idle\_timeout | _getter, setter_ | No docstring. |
| init\_args | _getter_ | No docstring. |
| init\_kwargs | _getter_ | No docstring. |
| initializer | _getter_ | No docstring. |
| max\_tasks\_per\_worker | _getter_ | No docstring. |
| max\_workers | _getter_ | No docstring. |
| mp\_context | _getter_ | No docstring. |
| name | _getter_ | No docstring. |
| terminated | _getter_ | No docstring. |
| worker\_type | _getter_ | No docstring. |
| workers | _getter_ | No docstring. |

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

# Methods within class
Here are methods exposed in the class:
- [\_\_init\_\_](#__init__)
- [check](#check)
- [count\_busy\_workers](#count_busy_workers)
- [count\_free\_workers](#count_free_workers)
- [count\_pending\_tasks](#count_pending_tasks)
- [count\_workers](#count_workers)
- [join](#join)
- [map](#map)
- [map\_all](#map_all)
- [run](#run)
- [shutdown](#shutdown)
- [spawn\_max\_workers](#spawn_max_workers)
- [spawn\_workers](#spawn_workers)
- [starmap](#starmap)
- [starmap\_all](#starmap_all)
- [submit](#submit)
- [test](#test)
- [\_cancel\_tasks](#_cancel_tasks)
- [\_cleanup\_cached\_futures](#_cleanup_cached_futures)
- [\_cleanup\_task\_queue](#_cleanup_task_queue)
- [\_count\_busy\_workers](#_count_busy_workers)
- [\_count\_free\_workers](#_count_free_workers)
- [\_count\_pending\_tasks](#_count_pending_tasks)
- [\_count\_workers](#_count_workers)
- [\_create\_lock](#_create_lock)
- [\_create\_worker](#_create_worker)
- [\_drain\_mp\_task\_queue](#_drain_mp_task_queue)
- [\_drain\_task\_queue](#_drain_task_queue)
- [\_ensure\_pool\_integrity](#_ensure_pool_integrity)
- [\_filter\_tasks](#_filter_tasks)
- [\_join\_inactive\_workers](#_join_inactive_workers)
- [\_join\_workers](#_join_workers)
- [\_map\_eager](#_map_eager)
- [\_map\_eager\_chunked](#_map_eager_chunked)
- [\_map\_lazy](#_map_lazy)
- [\_map\_lazy\_chunked](#_map_lazy_chunked)
- [\_map\_lazy\_chunked\_unordered](#_map_lazy_chunked_unordered)
- [\_map\_lazy\_unordered](#_map_lazy_unordered)
- [\_notify\_workers\_to\_shutdown](#_notify_workers_to_shutdown)
- [\_on\_worker\_exception](#_on_worker_exception)
- [\_on\_worker\_shutdown](#_on_worker_shutdown)
- [\_setup](#_setup)
- [\_shutdown\_filter\_thread](#_shutdown_filter_thread)
- [\_shutdown\_message\_thread](#_shutdown_message_thread)
- [\_spawn\_filter\_thread](#_spawn_filter_thread)
- [\_spawn\_workers](#_spawn_workers)
- [\_submit\_task](#_submit_task)

## \_\_init\_\_
Initialization.\x0a\x0a[param]\x0a- max_workers: the maximum number of workers. Defaults to CPU count + 5\x0a- name: the name of the pool. Defaults to the class name\x0a- idle_timeout: None or a timeout value in seconds.\x0a    The idle timeout tells how much time an inactive worker\x0a    can sleep before it closes. This helps the pool to shrink\x0a    when there isn't much of tasks.\x0a    If you set None, the pool will never shrink. each worker before it closes\x0a- initializer: a function that will get called at the start of each worker\x0a- init_args: arguments (list) to pass to the initializer\x0a- init_kwargs: keyword arguments (dict) to pass to the initializer\x0a- finalizer: a function that will get called when the worker is going to close\x0a- final_args: arguments (list) to pass to the finalizer\x0a- final_kwargs: keyword arguments (dict) to pass to the finalizer\x0a- max_tasks_per_worker: Maximum number of tasks a worker is allowed to do\x0a    before it closes.

```python
def __init__(self, *, name='DualThreadPool', idle_timeout=60, initializer=None, init_args=None, init_kwargs=None, finalizer=None, final_args=None, final_kwargs=None, max_tasks_per_worker=None):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## check
Check the pool\x0a\x0a[except]\x0a- RuntimeError: raised if the pool is closed\x0a- BrokenPoolError: raised if the pool is broken

```python
def check(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## count\_busy\_workers
Returns the number of busy workers

```python
def count_busy_workers(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## count\_free\_workers
Returns the number of free workers

```python
def count_free_workers(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## count\_pending\_tasks
Returns the number of pending tasks

```python
def count_pending_tasks(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## count\_workers
Returns the number of workers that are alive

```python
def count_workers(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## join
Join the workers, i.e., wait for workers to end their works, then close them\x0a\x0a[param]\x0a- timeout: None or a number representing seconds.\x0a\x0a[except]\x0a- RuntimeError: raised when timeout expires

```python
def join(self, timeout=None):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## map
Perform a Map operation lazily and return an iterator\x0athat iterates over the results.\x0aBeware, a remote exception will be reraised here\x0a\x0a[param]\x0a- target: callable\x0a- iterables: iterables to pass to the target\x0a- chunk_size: max length for a chunk\x0a- buffer_size: the buffer_size. A bigger size will consume more memory\x0a    but the overall operation will be faster\x0a- ordered: whether the original order should be kept or not\x0a- timeout: None or a timeout (int or float) value in seconds\x0a\x0a[return]\x0aReturns an iterator\x0a\x0a[except]\x0a- RuntimeError: raised when the pool is closed\x0a- BrokenPoolError: raised when the pool is broken\x0a- Exception: any remote exception

```python
def map(self, target, *iterables, chunk_size=1, buffer_size=1, ordered=True, timeout=None):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## map\_all
Perform a Map operation eagerly and return an iterator\x0athat iterates over the results.\x0aUsing this method instead of the `map` method might cause high memory usage.\x0aBeware, a remote exception will be reraised here\x0a\x0a[param]\x0a- target: callable\x0a- iterables: iterables to pass to the target\x0a- chunk_size: max length for a chunk\x0a- ordered: whether the original order should be kept or not\x0a- timeout: None or a timeout (int or float) value in seconds\x0a\x0a[return]\x0aReturns an iterator that iterates over the results.\x0a\x0a[except]\x0a- RuntimeError: raised when the pool is closed\x0a- BrokenPoolError: raised when the pool is broken\x0a- Exception: any remote exception

```python
def map_all(self, target, *iterables, chunk_size=1, ordered=True, timeout=None):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## run
Submit the task to the pool, and return\x0athe result (or re-raise the exception raised by the callable)\x0a\x0a[param]\x0a- target: callable\x0a- args: args to pass to the callable\x0a- kwargs: kwargs to pass to the callable\x0a\x0a[except]\x0a- RuntimeError: raised when the pool is closed\x0a- BrokenPoolError: raised when the pool is broken\x0a- Exception: exception that might be raised by the task itself

```python
def run(self, target, /, *args, **kwargs):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## shutdown
Close the pool by joining workers and cancelling pending tasks.\x0aNote that cancelled tasks can be retrieved via the cancelled_tasks property.\x0a\x0a[return]\x0aReturns False if the pool has already been closed, else returns True.

```python
def shutdown(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## spawn\_max\_workers
Spawn the maximum number of workers

```python
def spawn_max_workers(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## spawn\_workers
Spawn a specific number of workers or the right number\x0aof workers that is needed\x0a\x0a[param]\x0a- n: None or an integer.\x0a\x0a[return]\x0aReturns the number of spawned workers

```python
def spawn_workers(self, n=None):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## starmap
Perform a Starmap operation lazily and return an iterator\x0athat iterates over the results.\x0aBeware, a remote exception will be reraised here\x0a\x0a[param]\x0a- target: callable\x0a- iterable: sequence of args to pass to the target\x0a- chunk_size: max length for a chunk\x0a- buffer_size: the buffer_size. A bigger size will consume more memory\x0a    but the overall operation will be faster\x0a- ordered: whether the original order should be kept or not\x0a- timeout: None or a timeout (int or float) value in seconds\x0a\x0a[return]\x0aReturns an iterator that iterates over the results.\x0a\x0a[except]\x0a- RuntimeError: raised when the pool is closed\x0a- BrokenPoolError: raised when the pool is broken\x0a- Exception: any remote exception

```python
def starmap(self, target, iterable, chunk_size=1, buffer_size=1, ordered=True, timeout=None):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## starmap\_all
Perform a Starmap operation eagerly and return an iterator\x0athat iterates over the results.\x0aUsing this method instead of the `map` method might cause high memory usage.\x0aBeware, a remote exception will be reraised here\x0a\x0a[param]\x0a- target: callable\x0a- iterable: sequence of args to pass to the target\x0a- chunk_size: max length for a chunk\x0a- ordered: whether the original order should be kept or not\x0a- timeout: None or a timeout (int or float) value in seconds\x0a\x0a[return]\x0aReturns an iterator that iterates over the results.\x0a\x0a[except]\x0a- RuntimeError: raised when the pool is closed\x0a- BrokenPoolError: raised when the pool is broken\x0a- Exception: any remote exception

```python
def starmap_all(self, target, iterable, chunk_size=1, ordered=True, timeout=None):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## submit
Submit the task to the pool, and return\x0aa future object\x0a\x0a[param]\x0a- target: callable\x0a- args: args to pass to the callable\x0a- kwargs: kwargs to pass to the callable\x0a\x0a[except]\x0a- RuntimeError: raised when the pool is closed\x0a- BrokenPoolError: raised when the pool is broken\x0a- Exception: exception that might be raised by the task itself

```python
def submit(self, target, /, *args, **kwargs):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## test
Test the pool by creating another pool with the same config\x0aand doing some computation on it to ensure that it won't break.\x0aThis method might raise a BrokenPoolError exception

```python
def test(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_cancel\_tasks
No docstring

```python
def _cancel_tasks(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_cleanup\_cached\_futures
No docstring

```python
def _cleanup_cached_futures(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_cleanup\_task\_queue
No docstring

```python
def _cleanup_task_queue(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_count\_busy\_workers
No docstring

```python
def _count_busy_workers(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_count\_free\_workers
No docstring

```python
def _count_free_workers(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_count\_pending\_tasks
No docstring

```python
def _count_pending_tasks(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_count\_workers
No docstring

```python
def _count_workers(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_create\_lock
No docstring

```python
def _create_lock(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_create\_worker
No docstring

```python
def _create_worker(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_drain\_mp\_task\_queue
No docstring

```python
def _drain_mp_task_queue(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_drain\_task\_queue
No docstring

```python
def _drain_task_queue(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_ensure\_pool\_integrity
No docstring

```python
def _ensure_pool_integrity(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_filter\_tasks
No docstring

```python
def _filter_tasks(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_join\_inactive\_workers
No docstring

```python
def _join_inactive_workers(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_join\_workers
No docstring

```python
def _join_workers(self, timeout=None):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_map\_eager
No docstring

```python
def _map_eager(self, target, iterable, keep_order, timeout):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_map\_eager\_chunked
No docstring

```python
def _map_eager_chunked(self, target, iterable, chunk_size, keep_order, timeout):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_map\_lazy
No docstring

```python
def _map_lazy(self, target, iterable, buffer_size, timeout):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_map\_lazy\_chunked
No docstring

```python
def _map_lazy_chunked(self, target, iterable, chunk_size, buffer_size, timeout):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_map\_lazy\_chunked\_unordered
No docstring

```python
def _map_lazy_chunked_unordered(self, target, iterable, chunk_size, buffer_size, timeout):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_map\_lazy\_unordered
No docstring

```python
def _map_lazy_unordered(self, target, iterable, buffer_size, timeout):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_notify\_workers\_to\_shutdown
No docstring

```python
def _notify_workers_to_shutdown(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_on\_worker\_exception
No docstring

```python
def _on_worker_exception(self, worker_id, exc):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_on\_worker\_shutdown
No docstring

```python
def _on_worker_shutdown(self, worker_id):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_setup
No docstring

```python
def _setup(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_shutdown\_filter\_thread
No docstring

```python
def _shutdown_filter_thread(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_shutdown\_message\_thread
No docstring

```python
def _shutdown_message_thread(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_spawn\_filter\_thread
No docstring

```python
def _spawn_filter_thread(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_spawn\_workers
No docstring

```python
def _spawn_workers(self, n=None):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_submit\_task
No docstring

```python
def _submit_task(self, target, *args, **kwargs):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>
