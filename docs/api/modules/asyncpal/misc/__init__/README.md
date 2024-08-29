###### Asyncpal API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | Module | [Source](/asyncpal/misc/__init__.py)

# Module Overview
> Module: **asyncpal.misc.\_\_init\_\_**

Misc functions and classes.

## Fields
- [**All fields**](/docs/api/modules/asyncpal/misc/__init__/fields.md)
    - LOGGER = `<Logger asyncpal (WARNING)>`

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## Functions
- [**All functions**](/docs/api/modules/asyncpal/misc/__init__/funcs.md)
    - [get\_chunks](/docs/api/modules/asyncpal/misc/__init__/funcs.md#get_chunks): Split an iterable into chunks
    - [split\_map\_task](/docs/api/modules/asyncpal/misc/__init__/funcs.md#split_map_task): Split a map task into subtasks that don't take any arguments. The iterables are chunked according to chunk_size.
    - [split\_starmap\_task](/docs/api/modules/asyncpal/misc/__init__/funcs.md#split_starmap_task): Split a starmap task into subtasks that don't take any arguments. The iterable is chunked according to chunk_size.

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## Classes
- [**Countdown**](/docs/api/modules/asyncpal/misc/__init__/class-Countdown.md): Class to continually update a timeout as time passes. Used a lot by pools for map operations
    - [instant\_a](/docs/api/modules/asyncpal/misc/__init__/class-Countdown.md#properties-table); _getter_
    - [instant\_b](/docs/api/modules/asyncpal/misc/__init__/class-Countdown.md#properties-table); _getter_
    - [timeout](/docs/api/modules/asyncpal/misc/__init__/class-Countdown.md#properties-table); _getter_
    - [check](/docs/api/modules/asyncpal/misc/__init__/class-Countdown.md#check): Returns a new timeout value at each call
    - [get\_instant](/docs/api/modules/asyncpal/misc/__init__/class-Countdown.md#get_instant): Returns an instant value

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>
