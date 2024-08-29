###### Asyncpal API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/asyncpal/future/__init__/README.md) | [Source](/asyncpal/future/__init__.py)

# Functions within module
> Module: [asyncpal.future.\_\_init\_\_](/docs/api/modules/asyncpal/future/__init__/README.md)

Here are functions exposed in the module:
- [as\_done](#as_done)
- [collect](#collect)
- [wait](#wait)

## as\_done
Yields futures iteratively as they are done

```python
def as_done(futures, ordered=False, timeout=None):
    ...
```

| Parameter | Description |
| --- | --- |
| futures | sequence of futures |
| ordered | boolean to tell whether the results should be ordered or not |
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
