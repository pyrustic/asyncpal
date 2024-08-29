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
    - [get\_chunks](/docs/api/modules/asyncpal/misc/__init__/funcs.md#get_chunks): Split an iterable into chunks\x0a\x0a[param]\x0a- iterable: the iterable to split\x0a- chunk_size: max length for a chunk\x0a\x0...
    - [split\_map\_task](/docs/api/modules/asyncpal/misc/__init__/funcs.md#split_map_task): Split a map task into subtasks that don't take any arguments.\x0aThe iterables are chunked according to chunk_size.\x0a\x0a[para...
    - [split\_starmap\_task](/docs/api/modules/asyncpal/misc/__init__/funcs.md#split_starmap_task): Split a starmap task into subtasks that don't take any arguments.\x0aThe iterable is chunked according to chunk_size.\x0a\x0a[pa...

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## Classes
- [**Countdown**](/docs/api/modules/asyncpal/misc/__init__/class-Countdown.md): Class to continually update a timeout as time passes.\x0aUsed a lot by pools for map operations
    - [instant\_a](/docs/api/modules/asyncpal/misc/__init__/class-Countdown.md#properties-table); _getter_
    - [instant\_b](/docs/api/modules/asyncpal/misc/__init__/class-Countdown.md#properties-table); _getter_
    - [timeout](/docs/api/modules/asyncpal/misc/__init__/class-Countdown.md#properties-table); _getter_
    - [check](/docs/api/modules/asyncpal/misc/__init__/class-Countdown.md#check): Returns a new timeout value at each call
    - [get\_instant](/docs/api/modules/asyncpal/misc/__init__/class-Countdown.md#get_instant): Returns an instant value

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>
