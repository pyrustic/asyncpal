###### Asyncpal API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/asyncpal/future/__init__/README.md) | [Source](/asyncpal/future/__init__.py)

# Class Future
> Module: [asyncpal.future.\_\_init\_\_](/docs/api/modules/asyncpal/future/__init__/README.md)
>
> Class: **Future**
>
> Inheritance: `object`

Future class

## Properties table
Here are properties exposed in the class:

| Property | Methods | Description |
| --- | --- | --- |
| callbacks | _getter_ | No docstring. |
| cancel\_flag | _getter_ | No docstring. |
| cancelled | _getter_ | No docstring. |
| completed | _getter_ | No docstring. |
| done | _getter_ | No docstring. |
| duration | _getter_ | No docstring. |
| exception | _getter_ | No docstring. |
| failed | _getter_ | No docstring. |
| pending | _getter_ | No docstring. |
| pool | _getter_ | No docstring. |
| result | _getter_ | No docstring. |
| running | _getter_ | No docstring. |
| task\_id | _getter_ | No docstring. |

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

# Methods within class
Here are methods exposed in the class:
- [\_\_init\_\_](#__init__)
- [add\_callback](#add_callback)
- [add\_callbacks](#add_callbacks)
- [cancel](#cancel)
- [collect](#collect)
- [remove\_callback](#remove_callback)
- [remove\_callbacks](#remove_callbacks)
- [set\_exception](#set_exception)
- [set\_result](#set_result)
- [set\_status](#set_status)
- [wait](#wait)
- [\_execute\_callbacks](#_execute_callbacks)
- [\_update\_pending\_duration](#_update_pending_duration)
- [\_update\_task\_duration](#_update_task_duration)

## \_\_init\_\_
This class shouldn't be instantiated by the programmer

```python
def __init__(self, pool, task_id):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## add\_callback
Add one callback that accepts the future as argument.\x0a\x0a[param]\x0a- callback: the callback to add

```python
def add_callback(self, callback):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## add\_callbacks
Add a sequence of callbacks that accept the future as argument.\x0a\x0a[param]\x0a- callbacks: sequence of callbacks

```python
def add_callbacks(self, callbacks):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## cancel
Tries to cancel the linked task.\x0aNote that right after, the cancel_flag property is set to True\x0aand later, the cancelled property will be set to True or not.

```python
def cancel(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## collect
Collect the result of the task.\x0aBeware, a remote exception as well as CancelledError,\x0aor TimeoutError exceptions may be raised.\x0a\x0a[param]\x0a- timeout: None or a timeout value (int or float) in seconds.\x0a\x0a[return]\x0aReturns the collected result\x0a\x0a[except]\x0a- TimeoutError: raised when timeout expires\x0a- CancelledError: raised when a task got cancelled\x0a- Exception: any remote exception. Note that the __context__\x0aattribute of a remote exception contains an instance of\x0athe RemoteError class. The RemoteError class exposes via\x0aits exc_chain, the exception chain. Applying the builtin\x0a'str' function on the RemoteError object will return\x0athe remote traceback as a string.

```python
def collect(self, timeout=None):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## remove\_callback
Remove a callback\x0a\x0a[param]\x0a- callback: the callback to remove

```python
def remove_callback(self, callback):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## remove\_callbacks
Remove a sequence of callbacks\x0a\x0a[param]\x0a- callbacks: sequence of callbacks

```python
def remove_callbacks(self, callbacks):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## set\_exception
Private method ! Don't call it !

```python
def set_exception(self, exc, instant=None):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## set\_result
Private method ! Don't call it !

```python
def set_result(self, result, instant=None):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## set\_status
Private method ! Don't call it !

```python
def set_status(self, status, instant=None):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## wait
Wait (blocking) for the future to be done (completed, failed, or cancelled).\x0a\x0a[param]\x0a- timeout: None or a timeout value (int or float) in seconds.\x0a\x0a[return]\x0aReturns True if the future is done in the provided timeout range.

```python
def wait(self, timeout=None):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_execute\_callbacks
No docstring

```python
def _execute_callbacks(self, callbacks):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_update\_pending\_duration
No docstring

```python
def _update_pending_duration(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_update\_task\_duration
No docstring

```python
def _update_task_duration(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>
