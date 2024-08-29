###### Asyncpal API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | [Module](/docs/api/modules/asyncpal/misc/__init__/README.md) | [Source](/asyncpal/misc/__init__.py)

# Functions within module
> Module: [asyncpal.misc.\_\_init\_\_](/docs/api/modules/asyncpal/misc/__init__/README.md)

Here are functions exposed in the module:
- [get\_chunks](#get_chunks)
- [split\_map\_task](#split_map_task)
- [split\_starmap\_task](#split_starmap_task)

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
