###### Asyncpal API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | Module | [Source](/asyncpal/future/__init__.py)

# Module Overview
> Module: **asyncpal.future.\_\_init\_\_**

In this module are defined the `Future` and the `FutureFilter`
classes as well as the `wait`, `collect`, and `as_done` functions

## Functions
- [**All functions**](/docs/api/modules/asyncpal/future/__init__/funcs.md)
    - [as\_done](/docs/api/modules/asyncpal/future/__init__/funcs.md#as_done): Yields futures iteratively as they are done
    - [collect](/docs/api/modules/asyncpal/future/__init__/funcs.md#collect): Collect the results of a sequence of futures. Beware, remote exceptions as well as CancelledError, or TimeoutError exceptions mi...
    - [wait](/docs/api/modules/asyncpal/future/__init__/funcs.md#wait): Wait (blocking) for futures to get done (completed, failed, or cancelled).

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
    - [add\_callback](/docs/api/modules/asyncpal/future/__init__/class-Future.md#add_callback): Add one callback that accepts the future as argument.
    - [add\_callbacks](/docs/api/modules/asyncpal/future/__init__/class-Future.md#add_callbacks): Add a sequence of callbacks that accept the future as argument.
    - [cancel](/docs/api/modules/asyncpal/future/__init__/class-Future.md#cancel): Tries to cancel the linked task. Note that right after, the cancel_flag property is set to True and later, the cancelled propert...
    - [collect](/docs/api/modules/asyncpal/future/__init__/class-Future.md#collect): Collect the result of the task. Beware, a remote exception as well as CancelledError, or TimeoutError exceptions may be raised.
    - [remove\_callback](/docs/api/modules/asyncpal/future/__init__/class-Future.md#remove_callback): Remove a callback
    - [remove\_callbacks](/docs/api/modules/asyncpal/future/__init__/class-Future.md#remove_callbacks): Remove a sequence of callbacks
    - [set\_exception](/docs/api/modules/asyncpal/future/__init__/class-Future.md#set_exception): Private method ! Don't call it !
    - [set\_result](/docs/api/modules/asyncpal/future/__init__/class-Future.md#set_result): Private method ! Don't call it !
    - [set\_status](/docs/api/modules/asyncpal/future/__init__/class-Future.md#set_status): Private method ! Don't call it !
    - [wait](/docs/api/modules/asyncpal/future/__init__/class-Future.md#wait): Wait (blocking) for the future to be done (completed, failed, or cancelled).
    - [\_execute\_callbacks](/docs/api/modules/asyncpal/future/__init__/class-Future.md#_execute_callbacks): No docstring.
    - [\_update\_pending\_duration](/docs/api/modules/asyncpal/future/__init__/class-Future.md#_update_pending_duration): No docstring.
    - [\_update\_task\_duration](/docs/api/modules/asyncpal/future/__init__/class-Future.md#_update_task_duration): No docstring.
- [**FutureFilter**](/docs/api/modules/asyncpal/future/__init__/class-FutureFilter.md): This is a filter. First, you populate it with Future objects, then you retrieve futures as they are done. You can also retrieve ...
    - [futures](/docs/api/modules/asyncpal/future/__init__/class-FutureFilter.md#properties-table); _getter_
    - [get](/docs/api/modules/asyncpal/future/__init__/class-FutureFilter.md#get): Retrieve just one future that is done.
    - [get\_all](/docs/api/modules/asyncpal/future/__init__/class-FutureFilter.md#get_all): Yield futures as they are done until the filter is empty
    - [populate](/docs/api/modules/asyncpal/future/__init__/class-FutureFilter.md#populate): Populate the filter
    - [put](/docs/api/modules/asyncpal/future/__init__/class-FutureFilter.md#put): Add a future to the filter
    - [\_get\_from\_queue](/docs/api/modules/asyncpal/future/__init__/class-FutureFilter.md#_get_from_queue): No docstring.

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>
