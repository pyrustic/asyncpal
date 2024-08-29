###### Asyncpal API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/asyncpal/future/__init__/README.md) | [Source](/asyncpal/future/__init__.py)

# Functions within module
> Module: [asyncpal.future.\_\_init\_\_](/docs/api/modules/asyncpal/future/__init__/README.md)

Here are functions exposed in the module:
- [as\_done](#as_done)
- [collect](#collect)
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

## wait
Wait (blocking) for futures to get done (completed, failed, or cancelled).\x0a\x0a[param]\x0a- futures: sequence of Future objects\x0a- timeout: None or a timeout value (int or float) in seconds.\x0a\x0a[return]\x0aReturns True if all Futures are done in the provided timeout range.

```python
def wait(futures, timeout=None):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>
