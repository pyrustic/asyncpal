###### Asyncpal API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/asyncpal/__init__/README.md) | [Source](/asyncpal/__init__.py)

# Functions within module
> Module: [asyncpal.\_\_init\_\_](/docs/api/modules/asyncpal/__init__/README.md)

Here are functions exposed in the module:
- [as\_done](#as_done)
- [collect](#collect)
- [get\_chunks](#get_chunks)
- [split\_map\_task](#split_map_task)
- [split\_starmap\_task](#split_starmap_task)
- [wait](#wait)

## as\_done
Yields futures iteratively as they are done\x0a\x0a[param]\x0a- futures: sequence of futures\x0a- ordered: boolean to tell whether the results should be ordered or not\x0a- timeout: None or a timeout value (int or float) in seconds.\x0a\x0a[except]\x0a- TimeoutError: raised when timeout expires

```python
def as_done(futures, ordered=False, timeout=None):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## collect
Collect the results of a sequence of futures.\x0aBeware, remote exceptions as well as CancelledError,\x0aor TimeoutError exceptions might be raised.\x0a\x0a[param]\x0a- futures: sequence of Future objects\x0a- timeout: None or a timeout value (int or float) in seconds.\x0a\x0a[return]\x0aReturns a tuple containing the ordered results\x0acollected from all the futures\x0a\x0a[except]\x0a- TimeoutError: raised when timeout expires\x0a- CancelledError: raised when a task got cancelled

```python
def collect(futures, timeout=None):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## get\_chunks
Split an iterable into chunks\x0a\x0a[param]\x0a- iterable: the iterable to split\x0a- chunk_size: max length for a chunk\x0a\x0a[return]\x0aReturns an iterator

```python
def get_chunks(iterable, chunk_size):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## split\_map\_task
Split a map task into subtasks that don't take any arguments.\x0aThe iterables are chunked according to chunk_size.\x0a\x0a[param]\x0a- target: the callable task\x0a- iterables: the map iterables to pass to target\x0a- chunk_size: the max length of a chunk\x0a\x0a[yield]\x0aIteratively get a subtask that don't accept any arguments

```python
def split_map_task(target, *iterables, chunk_size=1):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## split\_starmap\_task
Split a starmap task into subtasks that don't take any arguments.\x0aThe iterable is chunked according to chunk_size.\x0a\x0a[param]\x0a- target: the callable task\x0a- iterable: a sequence of tuples each representing args to pass to target\x0a- chunk_size: the max length of a chunk\x0a\x0a[yield]\x0aIteratively get a subtask that don't accept any arguments

```python
def split_starmap_task(target, iterable, chunk_size=1):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## wait
Wait (blocking) for futures to get done (completed, failed, or cancelled).\x0a\x0a[param]\x0a- futures: sequence of Future objects\x0a- timeout: None or a timeout value (int or float) in seconds.\x0a\x0a[return]\x0aReturns True if all Futures are done in the provided timeout range.

```python
def wait(futures, timeout=None):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>
