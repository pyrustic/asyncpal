###### Asyncpal API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | Module | [Source](/asyncpal/future/__init__.py)

# Module Overview
> Module: **asyncpal.future.\_\_init\_\_**

In this module is defined the `Future` and the `FutureFilter`\x0aclasses as well as the `wait`, `collect`, and `as_done` functions

## Fields
- [**All fields**](/docs/api/modules/asyncpal/future/__init__/fields.md)
    - errors = `<module 'asyncpal.errors' from '/home/alex/PycharmProjects/asyncpal/asyncpal/errors/__init__.py'>`
    - functools = `<module 'functools' from '/usr/local/lib/python3.8/functools.py'>`
    - misc = `<module 'asyncpal.misc' from '/home/alex/PycharmProjects/asyncpal/asyncpal/misc/__init__.py'>`
    - threading = `<module 'threading' from '/usr/local/lib/python3.8/threading.py'>`
    - time = `<module 'time' (built-in)>`

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## Functions
- [**All functions**](/docs/api/modules/asyncpal/future/__init__/funcs.md)
    - [as\_done](/docs/api/modules/asyncpal/future/__init__/funcs.md#as_done): Yields futures iteratively as they are done\x0a\x0a[param]\x0a- futures: sequence of futures\x0a- ordered: boolean to tell wheth...
    - [collect](/docs/api/modules/asyncpal/future/__init__/funcs.md#collect): Collect the results of a sequence of futures.\x0aBeware, remote exceptions as well as CancelledError,\x0aor TimeoutError excepti...
    - [wait](/docs/api/modules/asyncpal/future/__init__/funcs.md#wait): Wait (blocking) for futures to get done (completed, failed, or cancelled).\x0a\x0a[param]\x0a- futures: sequence of Future objec...

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## Classes
- [**Future**](/docs/api/modules/asyncpal/future/__init__/class-Future.md): Future class
    - [callbacks](/docs/api/modules/asyncpal/future/__init__/class-Future.md#properties-table); _getter_
    - [cancel\_flag](/docs/api/modules/asyncpal/future/__init__/class-Future.md#properties-table); _getter_
    - [cancelled](/docs/api/modules/asyncpal/future/__init__/class-Future.md#properties-table); _getter_
    - [completed](/docs/api/modules/asyncpal/future/__init__/class-Future.md#properties-table); _getter_
    - [done](/docs/api/modules/asyncpal/future/__init__/class-Future.md#properties-table); _getter_
    - [duration](/docs/api/modules/asyncpal/future/__init__/class-Future.md#properties-table); _getter_
    - [exception](/docs/api/modules/asyncpal/future/__init__/class-Future.md#properties-table); _getter_
    - [failed](/docs/api/modules/asyncpal/future/__init__/class-Future.md#properties-table); _getter_
    - [pending](/docs/api/modules/asyncpal/future/__init__/class-Future.md#properties-table); _getter_
    - [pool](/docs/api/modules/asyncpal/future/__init__/class-Future.md#properties-table); _getter_
    - [result](/docs/api/modules/asyncpal/future/__init__/class-Future.md#properties-table); _getter_
    - [running](/docs/api/modules/asyncpal/future/__init__/class-Future.md#properties-table); _getter_
    - [task\_id](/docs/api/modules/asyncpal/future/__init__/class-Future.md#properties-table); _getter_
    - [add\_callback](/docs/api/modules/asyncpal/future/__init__/class-Future.md#add_callback): Add one callback that accepts the future as argument.\x0a\x0a[param]\x0a- callback: the callback to add
    - [add\_callbacks](/docs/api/modules/asyncpal/future/__init__/class-Future.md#add_callbacks): Add a sequence of callbacks that accept the future as argument.\x0a\x0a[param]\x0a- callbacks: sequence of callbacks
    - [cancel](/docs/api/modules/asyncpal/future/__init__/class-Future.md#cancel): Tries to cancel the linked task.\x0aNote that right after, the cancel_flag property is set to True\x0aand later, the cancelled p...
    - [collect](/docs/api/modules/asyncpal/future/__init__/class-Future.md#collect): Collect the result of the task.\x0aBeware, a remote exception as well as CancelledError,\x0aor TimeoutError exceptions may be ra...
    - [remove\_callback](/docs/api/modules/asyncpal/future/__init__/class-Future.md#remove_callback): Remove a callback\x0a\x0a[param]\x0a- callback: the callback to remove
    - [remove\_callbacks](/docs/api/modules/asyncpal/future/__init__/class-Future.md#remove_callbacks): Remove a sequence of callbacks\x0a\x0a[param]\x0a- callbacks: sequence of callbacks
    - [set\_exception](/docs/api/modules/asyncpal/future/__init__/class-Future.md#set_exception): Private method ! Don't call it !
    - [set\_result](/docs/api/modules/asyncpal/future/__init__/class-Future.md#set_result): Private method ! Don't call it !
    - [set\_status](/docs/api/modules/asyncpal/future/__init__/class-Future.md#set_status): Private method ! Don't call it !
    - [wait](/docs/api/modules/asyncpal/future/__init__/class-Future.md#wait): Wait (blocking) for the future to be done (completed, failed, or cancelled).\x0a\x0a[param]\x0a- timeout: None or a timeout valu...
    - [\_execute\_callbacks](/docs/api/modules/asyncpal/future/__init__/class-Future.md#_execute_callbacks): No docstring.
    - [\_update\_pending\_duration](/docs/api/modules/asyncpal/future/__init__/class-Future.md#_update_pending_duration): No docstring.
    - [\_update\_task\_duration](/docs/api/modules/asyncpal/future/__init__/class-Future.md#_update_task_duration): No docstring.
- [**FutureFilter**](/docs/api/modules/asyncpal/future/__init__/class-FutureFilter.md): This is a filter. First, you populate it with Future\x0aobjects, then you retrieve futures as they are done.\x0aYou can also ret...
    - [futures](/docs/api/modules/asyncpal/future/__init__/class-FutureFilter.md#properties-table); _getter_
    - [get](/docs/api/modules/asyncpal/future/__init__/class-FutureFilter.md#get): Retrieve just one future that is done.\x0a\x0a[param]\x0a- block: boolean to block until one future is done\x0a- timeout: None o...
    - [get\_all](/docs/api/modules/asyncpal/future/__init__/class-FutureFilter.md#get_all): Yield futures as they are done until the filter is empty\x0a\x0a[param]\x0a- block: boolean to block until one future is done\x0...
    - [populate](/docs/api/modules/asyncpal/future/__init__/class-FutureFilter.md#populate): Populate the filter\x0a\x0a[param]\x0a- futures: sequence of Future object
    - [put](/docs/api/modules/asyncpal/future/__init__/class-FutureFilter.md#put): Add a future to the filter\x0a\x0a[param]\x0a- future: Future object
    - [\_get\_from\_queue](/docs/api/modules/asyncpal/future/__init__/class-FutureFilter.md#_get_from_queue): No docstring.
- [**Status**](/docs/api/modules/asyncpal/future/__init__/class-Status.md): An enumeration.
    - PENDING = `1`
    - RUNNING = `2`
    - COMPLETED = `3`
    - FAILED = `4`
    - CANCELLED = `5`

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>
