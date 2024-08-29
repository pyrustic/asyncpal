###### Asyncpal API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/asyncpal/errors/__init__/README.md) | [Source](/asyncpal/errors/__init__.py)

# Class RemoteError
> Module: [asyncpal.errors.\_\_init\_\_](/docs/api/modules/asyncpal/errors/__init__/README.md)
>
> Class: **RemoteError**
>
> Inheritance: [asyncpal.errors.Error](/docs/api/modules/asyncpal/errors/__init__/class-Error.md)

An object of this class is available on the\x0a__context__ attribute of any remote exception\x0ain a ProcessPool. This class has zero link with ThreadPool.

## Fields table
Here are fields exposed in the class:

| Field | Value |
| --- | --- |
| args | `<attribute 'args' of 'BaseException' objects>` |
| with\_traceback | `<method 'with_traceback' of 'BaseException' objects>` |

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## Properties table
Here are properties exposed in the class:

| Property | Methods | Description |
| --- | --- | --- |
| exc\_chain | _getter_ | No docstring. |

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

# Methods within class
Here are methods exposed in the class:
- [\_\_init\_\_](#__init__)

## \_\_init\_\_
Initialize self.  See help(type(self)) for accurate signature.

```python
def __init__(self, traceback_str, exc_chain):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>
