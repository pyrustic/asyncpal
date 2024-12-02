###### Asyncpal API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/asyncpal/future/__init__/README.md) | [Source](/src/asyncpal/future/__init__.py)

# Class Status
> Module: [asyncpal.future.\_\_init\_\_](/docs/api/modules/asyncpal/future/__init__/README.md)
>
> Class: **Status**
>
> Inheritance: `enum.Enum`

Create a collection of name/value pairs.

Example enumeration:

>>> class Color(Enum):
...     RED = 1
...     BLUE = 2
...     GREEN = 3

Access them by:

- attribute access:

  >>> Color.RED
  <Color.RED: 1>

- value lookup:

  >>> Color(1)
  <Color.RED: 1>

- name lookup:

  >>> Color['RED']
  <Color.RED: 1>

Enumerations can be iterated over, and know how many members they have:

>>> len(Color)
3

>>> list(Color)

## Fields table
Here are fields exposed in the class:

| Field | Value |
| --- | --- |
| PENDING | `1` |
| RUNNING | `2` |
| COMPLETED | `3` |
| FAILED | `4` |
| CANCELLED | `5` |

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

# Methods within class
Here are methods exposed in the class:
- [\_\_init\_\_](#__init__)
- [\_generate\_next\_value\_](#_generate_next_value_)
- [\_missing\_](#_missing_)

## \_\_init\_\_
Initialize self.  See help(type(self)) for accurate signature.

```python
def __init__(self, *args, **kwds):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_generate\_next\_value\_
Generate the next value when not given.

name: the name of the member
start: the initial start value or None
count: the number of existing members
last_values: the list of values assigned

```python
@staticmethod
def _generate_next_value_(name, start, count, last_values):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_missing\_
No docstring

```python
@classmethod
def _missing_(value):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>
