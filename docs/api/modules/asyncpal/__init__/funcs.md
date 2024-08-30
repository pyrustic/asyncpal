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
Yields futures iteratively as they are done

```python
def as_done(futures, keep_order=False, timeout=None):
    ...
```

| Parameter | Description |
| --- | --- |
| futures | sequence of futures |
| keep\_order | boolean to tell whether the results should be ordered or not |
| timeout | None or a timeout value (int or float) in seconds. |

### Exceptions table
The table below outlines exceptions that may occur.

| Exception | Circumstance |
| --- | --- |
| TimeoutError | raised when timeout expires |

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## collect
Collect the results of a sequence of futures.
Beware, remote exceptions as well as CancelledError,
or TimeoutError exceptions might be raised.

```python
def collect(futures, timeout=None):
    ...
```

| Parameter | Description |
| --- | --- |
| futures | sequence of Future objects |
| timeout | None or a timeout value (int or float) in seconds. |

### Value to return
Returns a tuple containing the ordered results
collected from all the futures

### Exceptions table
The table below outlines exceptions that may occur.

| Exception | Circumstance |
| --- | --- |
| TimeoutError | raised when timeout expires |
| CancelledError | raised when a task got cancelled |

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## get\_chunks
Split an iterable into chunks

```python
def get_chunks(iterable, chunk_size):
    ...
```

| Parameter | Description |
| --- | --- |
| iterable | the iterable to split |
| chunk\_size | max length for a chunk |

### Value to return
Returns an iterator

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## split\_map\_task
Split a map task into subtasks that don't take any arguments.
The iterables are chunked according to chunk_size.

```python
def split_map_task(target, *iterables, chunk_size=1):
    ...
```

| Parameter | Description |
| --- | --- |
| target | the callable task |
| iterables | the map iterables to pass to target |
| chunk\_size | the max length of a chunk |

### Value to yield
Iteratively get a subtask that don't accept any arguments

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## split\_starmap\_task
Split a starmap task into subtasks that don't take any arguments.
The iterable is chunked according to chunk_size.

```python
def split_starmap_task(target, iterable, chunk_size=1):
    ...
```

| Parameter | Description |
| --- | --- |
| target | the callable task |
| iterable | a sequence of tuples each representing args to pass to target |
| chunk\_size | the max length of a chunk |

### Value to yield
Iteratively get a subtask that don't accept any arguments

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## wait
Wait (blocking) for futures to get done (completed, failed, or cancelled).

```python
def wait(futures, timeout=None):
    ...
```

| Parameter | Description |
| --- | --- |
| futures | sequence of Future objects |
| timeout | None or a timeout value (int or float) in seconds. |

### Value to return
Returns True if all Futures are done in the provided timeout range.

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>
