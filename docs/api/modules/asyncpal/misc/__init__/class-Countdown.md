###### Asyncpal API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/asyncpal/misc/__init__/README.md) | [Source](/asyncpal/misc/__init__.py)

# Class Countdown
> Module: [asyncpal.misc.\_\_init\_\_](/docs/api/modules/asyncpal/misc/__init__/README.md)
>
> Class: **Countdown**
>
> Inheritance: `object`

Class to continually update a timeout as time passes.
Used a lot by pools for map operations

## Properties table
Here are properties exposed in the class:

| Property | Methods | Description |
| --- | --- | --- |
| instant\_a | _getter_ | Instant alpha: the instant the Countdown object is created |
| instant\_b | _getter_ | Instant beta: the exact instant the timeout expires.
Is None if the original timeout is None |
| timeout | _getter_ | No docstring. |

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

# Methods within class
Here are methods exposed in the class:
- [\_\_init\_\_](#__init__)
- [check](#check)
- [get\_instant](#get_instant)

## \_\_init\_\_
Init.

```python
def __init__(self, timeout):
    ...
```

| Parameter | Description |
| --- | --- |
| timeout | None or a timeout (int or float) value in seconds |

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## check
Returns a new timeout value at each call

```python
def check(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## get\_instant
Returns an instant value

```python
@staticmethod
def get_instant(self):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>
