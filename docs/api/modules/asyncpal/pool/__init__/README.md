###### Asyncpal API Reference
[Home](/docs/api/README.md) | [Project](/README.md) | Module | [Source](/asyncpal/pool/__init__.py)

# Module Overview
> Module: **asyncpal.pool.\_\_init\_\_**

The abstract base class for all pools is defined here,
as well as the GlobalShutdown class.

## Fields
- [**All fields**](/docs/api/modules/asyncpal/pool/__init__/fields.md)
    - IDLE\_TIMEOUT = `60`
    - MP\_CONTEXT = `<multiprocessing.context.SpawnContext object at 0x7f79ec29c9a0>`
    - WINDOWS\_MAX\_PROCESS\_WORKERS = `60`

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>

## Classes
- [**Pool**](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md): Helper class that provides a standard way to create an ABC using inheritance.
    - [\_abc\_impl](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#fields-table) = `<_abc_data object at 0x7f79eb93b630>`
    - [broken](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#properties-table); _getter_
    - [cancelled\_tasks](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#properties-table); _getter_
    - [closed](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#properties-table); _getter_
    - [final\_args](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#properties-table); _getter_
    - [final\_kwargs](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#properties-table); _getter_
    - [finalizer](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#properties-table); _getter_
    - [idle\_timeout](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#properties-table); _getter, setter_
    - [init\_args](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#properties-table); _getter_
    - [init\_kwargs](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#properties-table); _getter_
    - [initializer](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#properties-table); _getter_
    - [max\_tasks\_per\_worker](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#properties-table); _getter_
    - [max\_workers](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#properties-table); _getter_
    - [mp\_context](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#properties-table); _getter_
    - [name](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#properties-table); _getter_
    - [terminated](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#properties-table); _getter_
    - [worker\_type](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#properties-table); _getter_
    - [workers](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#properties-table); _getter_
    - [check](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#check): Check the pool
    - [count\_busy\_workers](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#count_busy_workers): Returns the number of busy workers
    - [count\_free\_workers](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#count_free_workers): Returns the number of free workers
    - [count\_pending\_tasks](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#count_pending_tasks): Returns the number of pending tasks
    - [count\_workers](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#count_workers): Returns the number of workers that are alive
    - [join](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#join): Join the workers, i.e., wait for workers to end their works, then close them
    - [map](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#map): Perform a Map operation lazily and return an iterator that iterates over the results. Beware, a remote exception will be reraise...
    - [map\_all](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#map_all): Perform a Map operation eagerly and return an iterator that iterates over the results. Using this method instead of the `map` me...
    - [run](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#run): Submit the task to the pool, and return the result (or re-raise the exception raised by the callable)
    - [shutdown](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#shutdown): Close the pool by joining workers and cancelling pending tasks. Note that cancelled tasks can be retrieved via the cancelled_tas...
    - [spawn\_max\_workers](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#spawn_max_workers): Spawn the maximum number of workers
    - [spawn\_workers](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#spawn_workers): Spawn a specific number of workers or the right number of workers that is needed
    - [starmap](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#starmap): Perform a Starmap operation lazily and return an iterator that iterates over the results. Beware, a remote exception will be rer...
    - [starmap\_all](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#starmap_all): Perform a Starmap operation eagerly and return an iterator that iterates over the results. Using this method instead of the `map...
    - [submit](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#submit): Submit the task to the pool, and return a future object
    - [test](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#test): Test the pool by creating another pool with the same config and doing some computation on it to ensure that it won't break. This...
    - [\_cancel\_tasks](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_cancel_tasks): No docstring.
    - [\_cleanup\_cached\_futures](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_cleanup_cached_futures): No docstring.
    - [\_cleanup\_task\_queue](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_cleanup_task_queue): No docstring.
    - [\_count\_busy\_workers](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_count_busy_workers): No docstring.
    - [\_count\_free\_workers](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_count_free_workers): No docstring.
    - [\_count\_pending\_tasks](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_count_pending_tasks): No docstring.
    - [\_count\_workers](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_count_workers): No docstring.
    - [\_create\_lock](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_create_lock): No docstring.
    - [\_create\_worker](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_create_worker): No docstring.
    - [\_drain\_mp\_task\_queue](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_drain_mp_task_queue): No docstring.
    - [\_drain\_task\_queue](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_drain_task_queue): No docstring.
    - [\_ensure\_pool\_integrity](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_ensure_pool_integrity): No docstring.
    - [\_filter\_tasks](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_filter_tasks): No docstring.
    - [\_join\_inactive\_workers](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_join_inactive_workers): No docstring.
    - [\_join\_workers](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_join_workers): No docstring.
    - [\_map\_eager](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_map_eager): No docstring.
    - [\_map\_eager\_chunked](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_map_eager_chunked): No docstring.
    - [\_map\_lazy](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_map_lazy): No docstring.
    - [\_map\_lazy\_chunked](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_map_lazy_chunked): No docstring.
    - [\_map\_lazy\_chunked\_unordered](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_map_lazy_chunked_unordered): No docstring.
    - [\_map\_lazy\_unordered](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_map_lazy_unordered): No docstring.
    - [\_notify\_workers\_to\_shutdown](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_notify_workers_to_shutdown): No docstring.
    - [\_on\_worker\_exception](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_on_worker_exception): No docstring.
    - [\_on\_worker\_shutdown](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_on_worker_shutdown): No docstring.
    - [\_setup](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_setup): No docstring.
    - [\_shutdown\_filter\_thread](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_shutdown_filter_thread): No docstring.
    - [\_shutdown\_message\_thread](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_shutdown_message_thread): No docstring.
    - [\_spawn\_filter\_thread](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_spawn_filter_thread): No docstring.
    - [\_spawn\_workers](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_spawn_workers): No docstring.
    - [\_submit\_task](/docs/api/modules/asyncpal/pool/__init__/class-Pool.md#_submit_task): No docstring.

<p align="right"><a href="#asyncpal-api-reference">Back to top</a></p>
