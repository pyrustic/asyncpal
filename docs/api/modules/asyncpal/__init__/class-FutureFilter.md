###### Asyncpal API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/asyncpal/__init__/README.md) | [Source](/asyncpal/__init__.py)

# Class FutureFilter
> Module: [asyncpal.\_\_init\_\_](/docs/api/modules/asyncpal/__init__/README.md)
>
> Class: **FutureFilter**
>
> Inheritance: `object`

This is a filter. First, you populate it with Future\x0aobjects, then you retrieve futures as they are done.\x0aYou can also retrieve futures while feeding the filter.\x0aThe original order of the futures doesn't matter here.\x0a\x0aThis class is used by the `as_done` function when its\x0aordered option is set to False.

## Properties table
Here are properties exposed in the class:

| Property | Methods | Description |
| --- | --- | --- |
| futures | _getter_ | No docstring. |

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

# Methods within class
Here are methods exposed in the class:
- [\_\_init\_\_](#__init__)
- [get](#get)
- [get\_all](#get_all)
- [populate](#populate)
- [put](#put)
- [\_get\_from\_queue](#_get_from_queue)

## \_\_init\_\_
Initialize self.  See help(type(self)) for accurate signature.

```python
def __init__(self, futures=None):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## get
Retrieve just one future that is done.\x0a\x0a[param]\x0a- block: boolean to block until one future is done\x0a- timeout: None or a timeout value (int or float) in seconds.\x0a\x0a[return]\x0aReturns a future object that is done

```python
def get(self, block=True, timeout=None):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## get\_all
Yield futures as they are done until the filter is empty\x0a\x0a[param]\x0a- block: boolean to block until one future is done\x0a- timeout: None or a timeout value (int or float) in seconds.\x0a\x0a[yield]\x0aYield a future object that is done until the filter is empty

```python
def get_all(self, block=True, timeout=None):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## populate
Populate the filter\x0a\x0a[param]\x0a- futures: sequence of Future object

```python
def populate(self, futures):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## put
Add a future to the filter\x0a\x0a[param]\x0a- future: Future object

```python
def put(self, future):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## \_get\_from\_queue
No docstring

```python
def _get_from_queue(self, block, timeout):
    ...
```

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>
