###### Asyncpal API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/asyncpal/errors/__init__/README.md) | [Source](/src/asyncpal/errors/__init__.py)

# Class RemoteTraceback
> Module: [asyncpal.errors.\_\_init\_\_](/docs/api/modules/asyncpal/errors/__init__/README.md)
>
> Class: **RemoteTraceback**
>
> Inheritance: [asyncpal.errors.Error](/docs/api/modules/asyncpal/errors/__init__/class-Error.md)

An instance of this class is available on the
__context__ attribute of the last remote exception in an
exception chain that occurred in a ProcessPool.

## Fields table
Here are fields exposed in the class:

| Field | Value |
| --- | --- |
| add\_note | `<method 'add_note' of 'BaseException' objects>` |
| args | `<attribute 'args' of 'BaseException' objects>` |
| with\_traceback | `<method 'with_traceback' of 'BaseException' objects>` |

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## Properties table
Here are properties exposed in the class:

| Property | Methods | Description |
| --- | --- | --- |
| traceback\_lines | _getter_ | No docstring. |

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

# Methods within class
Here are methods exposed in the class:
- [\_\_init\_\_](#__init__)

## \_\_init\_\_
Initialize self.  See help(type(self)) for accurate signature.

```python
def __init__(self, traceback_lines):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>
