[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI package version](https://img.shields.io/pypi/v/asyncpal)](https://pypi.org/project/asyncpal)
[![Downloads](https://static.pepy.tech/badge/asyncpal)](https://pepy.tech/project/asyncpal)


<!-- Cover -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/assets/asyncpal/cover.jpg" alt="Cover image" width="640">
    <p align="center">
        <a href="https://commons.wikimedia.org/wiki/File:Carrera_de_carros_romanos.jpg">Poniol</a>, <a href="https://creativecommons.org/licenses/by-sa/3.0">CC BY-SA 3.0</a>, via Wikimedia Commons
    </p>
</div>

<!-- Intro Text -->
# Asyncpal
<b>Preemptive concurrency and parallelism for sporadic workloads</b>

## Table of contents
- [Overview](#overview)
    - [Designed for sporadic workloads](#designed-for-sporadic-workloads)
    - [Supplied with advanced capabilities](#supplied-with-advanced-capabilities)
    - [Featuring a familiar interface](#featuring-a-familiar-interface)
- [Examples](#examples)
- [Embarrassingly parallel workloads](#embarrassingly-parallel-workloads)
- [Initializers, finalizers, and the BrokenPoolError exception](#initializers-finalizers-and-the-brokenpoolerror-exception)
- [The peculiar cases of daemons and remote exceptions](#the-peculiar-cases-of-daemons-and-remote-exceptions)
- [Application programming interface](#application-programming-interface)
    - [ThreadPool class](#threadpool-class)
    - [ProcessPool class](#processpool-class)
    - [Future class](#future-class)
    - [Miscellaneous functions and classes](#miscellaneous-functions-and-classes)
    - [Exception classes](#exception-classes)
- [Testing and contributing](#testing-and-contributing)
- [Installation](#installation)


# Overview
**Asyncpal** is a [Python](https://www.python.org/) library designed for preemptive [concurrency](https://en.wikipedia.org/wiki/Concurrent_computing) and [parallelism](https://en.wikipedia.org/wiki/Parallel_computing). It achieves concurrency using the [thread pool](https://en.wikipedia.org/wiki/Thread_pool) design pattern that it extends with processes to enable parallelism.

## Designed for sporadic workloads
Although a thread pool is the right tool for the problems it solves, its creation and usage involve the allocation of resources that must be properly released. For this reason, it is recommended to use a thread pool with a context manager to ensure that resources are properly released once the pool executor has finished the tasks.

However, this strategy can introduce overhead in programs that sporadically submit tasks to a thread pool, as multiple pools may be created and destroyed throughout the execution of these programs.

Maintaining one or a few thread pools for the duration of a program can be an effective solution, assuming these thread pools can automatically **shrink** after workers have been idle for a short period defined by the programmer.

Asyncpal offers the ability to set an idle timeout for workers, allowing the pool to which they belong to shrink when they are not in use.

> Learn how Asyncpal ensures a [graceful shutdown](#the-peculiar-case-of-daemons) of open pools when an uncaught exception occurs.

## Supplied with advanced capabilities
Asyncpal pools provide methods to manage [embarrassingly parallel workloads](https://en.wikipedia.org/wiki/Embarrassingly_parallel), allowing for lazy or eager execution and optional workload splitting into large chunks, with or without preserving their original order.

Some level of introspection is achievable directly from the pool interface, such as counting busy workers or pending tasks. Additionally, a `Future` class (never directly instantiated by the user) is provided, whose objects allow a task to be cancelled or its result to be collected. Furthermore, the pending time and running duration of a task can be obtained directly from a `Future` object.

Overall, the characteristics of Asyncpal make it suitable for both implicit use in the background through higher-level abstractions provided by frameworks or libraries, and for explicit use with or without a context manager.

## Featuring a familiar interface
Asyncpal is inspired by the great preemptive concurrency and parallelism packages provided in Python and Java.

For instance, the `chunk_size` option for map operations is borrowed from Python's [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) and [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html) packages, while the fixed-size pools, such as the `SingleThreadPool` class, are inspired by Java's [java.util.concurrent.Executors.newSingleThreadExecutor](https://docs.oracle.com/en%2Fjava%2Fjavase%2F22%2Fdocs%2Fapi%2F%2F/java.base/java/util/concurrent/Executors.html#newSingleThreadExecutor()) static method.


# Examples
The following code snippets are adapted from examples provided by Python's `concurrent.futures` documentation page.

## Thread pool example
The following code snippet is adapted from [ThreadPoolExecutor example](https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor-example) provided by Python's concurrent.futures documentation [page](https://docs.python.org/3/library/concurrent.futures.html).

```python
import urllib.request
from asyncpal import ThreadPool, as_done

URLS = ["https://ubuntu.com/",
        "https://github.com/pyrustic/asyncpal/",
        "https://youtu.be/xLi83prR5fg",
        "https://news.ycombinator.com/",
        "https://nonexistant-subdomain.python.org/"]

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()

# Thread pool with a context manager (not mandatory, tho)
with ThreadPool(max_workers=5) as pool:
    # Start the load operations and mark each future with its URL
    future_to_url = {pool.submit(load_url, url, 60): url for url in URLS}
    for future in as_done(future_to_url):
        url = future_to_url[future]
        try:
            data = future.collect()  # collect the result or raise the exception
        except Exception as exc:
            print("%r generated an exception: %s" % (url, exc))
        else:
            print("%r page is %d bytes" % (url, len(data)))
```

> The function `as_done` accepts a list of Future objects and also the `keep_order` and `timeout` keyword arguments.

## Process pool example
The following code snippet is adapted from [ProcessPoolExecutor example](https://docs.python.org/3/library/concurrent.futures.html#processpoolexecutor-example) provided by Python's concurrent.futures documentation [page](https://docs.python.org/3/library/concurrent.futures.html).

```python
import math
from asyncpal import ProcessPool

PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def main():
    with ProcessPool() as pool:
        # The 'map' method is lazy and slower than 'map_all'.
        # For very long iterables, 'map_all' may cause high memory usage.
        for number, prime in zip(PRIMES, pool.map(is_prime, PRIMES)):
            print("%d is prime: %s" % (number, prime))

if __name__ == "__main__":
    main()
```

> The method `map` also accepts these keyword arguments: `chunk_size`, `buffer_size`, `keep_order`, and `timeout`.


# Embarrassingly parallel workloads
Asyncpal pool classes provide four methods to perform [Map](https://en.wikipedia.org/wiki/Map_(parallel_pattern)) operations and for cases where control is more important than convenience, there are public functions for manually splitting a task into subtasks to submit to the pool.

## Pool class methods to perform Map operations
Pool class methods to perform Map operations are `map`, `map_all`, `starmap`, and `starmap_all`.

```python
from itertools import starmap
from asyncpal import ThreadPool

def add(x, y):
    return x + y

with ThreadPool(4) as pool:
    # numbers go from 0 to 99
    numbers = range(100)

    # The 'map' method is lazy and slower than 'map_all'.
    # Keyword arguments: chunk_size, buffer_size, keep_order, timeout
    iterator = pool.map(add, numbers, numbers, chunk_size=25)
    assert tuple(iterator) == tuple(map(add, numbers, numbers))

    # For very long iterables, 'map_all' may cause high memory usage.
    # Keyword arguments: chunk_size, keep_order, timeout
    iterator = pool.map_all(add, numbers, numbers, chunk_size=25)
    assert tuple(iterator) == tuple(map(add, numbers, numbers))

    # The 'starmap' method is lazy and slower than 'starmap_all'.
    # Keyword arguments: chunk_size, buffer_size, keep_order, timeout
    iterator = pool.starmap(add, zip(numbers, numbers), chunk_size=25)
    assert tuple(iterator) == tuple(starmap(add, zip(numbers, numbers)))

    # For very long iterables, 'starmap_all' may cause high memory usage.
    # Keyword arguments: chunk_size, keep_order, timeout
    iterator = pool.starmap_all(add, zip(numbers, numbers), chunk_size=25)
    assert tuple(iterator) == tuple(starmap(add, zip(numbers, numbers)))
```

> For convenience, there are also `map_unordered`, `map_all_unordered`, `starmap_unordered`, `starmap_all_unordered`.

## Useful functions
The `split_map_task` and `split_starmap_task` functions allow to manually split a task into subtasks. There are also the `wait`, `collect` and `as_done` functions which are intended to be applied to sequences of Future objects.

```python
from asyncpal import (ThreadPool, split_map_task, split_starmap_task,
                      wait, collect, as_done)

def add(x, y):
    return x + y

with ThreadPool(4) as pool:
    # numbers go from 0 to 99
    numbers = range(100)

    # Manually split a 'map' task into 4 subtasks
    futures = list()
    for subtask in split_map_task(add, numbers, numbers, chunk_size=25):
        future = pool.submit(subtask)
        futures.append(future)

    # We could've used 'split_starmap_task'
    for subtask in split_starmap_task(add, zip(numbers, numbers)):
        pass

    # We can block the current thread, waiting for the results to be available
    wait(futures, timeout=42)  # 42 seconds !

    # Or we can just collect results (beware, an exception may be raised)
    result = list()
    for sub_result in collect(futures, timeout=42):
        result.extend(sub_result)
    assert tuple(result) == tuple(map(add, numbers, numbers))

    # We could've used 'as_done' to filter out futures as they are done.
    # Note that by default, the keyword argument 'keep_order' is False !
    for future in as_done(futures, timeout=42):
        pass
```

# Initializers, finalizers, and the BrokenPoolError exception
At the creation of a pool, the programmer can provide an initializer and/or a finalizer. Consequently, each time the pool spawns a worker (whether it is a thread or a process), the initializer is executed at startup, and the finalizer is executed right before the worker shuts down.

Any exception raised during initialization, finalization, or in between will be caught by the pool, which will then enter a "broken" state. Once the pool is broken, it will shut down other workers, cancel pending tasks, and make them available via the `cancelled_tasks` property. It will also raise a `BrokenPoolError` exception whenever the programmer attempts to submit new tasks. 

Asyncpal offers a way to reduce the risk of encountering a `BrokenPoolError` exception at an inconvenient time by testing the pool beforehand. All pool classes provide a `test` method that replicate the pool with its configuration, perform some computation on it, then close it, letting any exception propagate to the top.

# The peculiar cases of daemons and remote exceptions
This section discusses the peculiar cases of daemons and remote exceptions.

## The peculiar case of daemons
In Python, a thread can be flagged as a [daemon thread](https://docs.python.org/3/library/threading.html#thread-objects). The significance of this flag is that the entire Python program exits when only daemon threads are left.

Prior to **Python 3.9**, `concurrent.futures` used daemon threads as workers for its thread pool and relied on [atexit](https://docs.python.org/3/library/atexit.html) hooks to gracefully shut down the pools that had not been explicitly closed. For compatibility with subinterpreters, which do not support daemon threads, it was decided to [remove the daemon flag](https://docs.python.org/3/whatsnew/3.9.html#concurrent-futures). However, simply removing the daemon flag would have been [problematic](https://bugs.python.org/issue37266#msg362890). 

The fix for this issue involved stopping the use of atexit hooks and instead relying on an [internal threading atexit hook](https://bugs.python.org/issue37266#msg362960). Asyncpal does not use the daemon flag either. Instead of relying on some internal Python function that might disappear without warning, it implements its own workaround. This workaround involves a single thread for the entire program, started by `asyncpal.pool.GlobalShutdown`, whose job is to join the main thread and, once joined, run the shutdown handlers registered by the pools. 

> Feel free to open an issue to criticize this workaround or to suggest a better idea.

## The peculiar case of remote exceptions
An exception raised in a worker of a `ProcessPool` must go through a multiprocessing queue to reach the pool instance. To be placed in a multiprocessor queue, a Python object must be **picklable**, that is, it must be possible to [serialize](https://en.wikipedia.org/wiki/Serialization) it with Python's [pickle](https://docs.python.org/3/library/pickle.html) mechanism.

An exception instance typically contains a traceback object that is not picklable and thus nullified by the `pickle` mechanism. Python's `concurrent.futures` and `multiprocessing.pool.Pool` use a hack that stringifies traceback to move it from the worker process to the main pool process.

Although this hack is interesting and useful for debugging a `ProcessPool`, it does not preserve the chain of exceptions because the `pickling` process not only nullifies the `__traceback__` attribute of the exception object, but also the `__cause__` and `__context__` attributes.

Asyncpal also stringifies the traceback, as it is a simpler solution than recreating the traceback object in the main process. Additionally, Asyncpal replicates the exception chain, so the programmer can navigate through the `__cause__` and `__context__` attributes of a remote exception.

> The `get_remote_traceback` function is exposed to quickly extract the traceback string of a remote exception.


# Application programming interface
> This section describes the API and refers to the API reference for more details.

Asyncpal consists of three key components: the **Pool**, the **Worker**, and the **Future**. From the programmer perspective, the pool represents the main interface of a system that spawns workers as needed and returns Future objects.

Preemptive concurrency is achieved with the `ThreadPool` class while parallelism is handled by the `ProcessPool` class. Under the hood, the thread pool spawns Python's `threading.Thread` as workers and the process pool spawns Python's `multiprocessing.Process` as workers.


## ThreadPool class
Preemptive concurrency is achieved with the `ThreadPool` class. Under the hood, the thread pool spawns Python's `threading.Thread` as workers.

For convenience, the following four derived classes are provided:

- `SingleThreadPool`: spawns only 1 worker
- `DualThreadPool`: spawns up to 2 workers
- `TripleThreadPool`: spawns up to 3 workers
- `QuadThreadPool`: spawns up to 4 workers

```python
from asyncpal import ThreadPool
from asyncpal.errors import BrokenPoolError, InitializerError, FinalizerError


def add(x, y):
  return x + y


def initializer(*args, **kwargs):
  pass


def finalizer(*args, **kwargs):
  pass


# all these arguments are optional
pool = ThreadPool(max_workers=4, name="my-pool", idle_timeout=60,
                  initializer=initializer, init_args=(1, 2),
                  init_kwargs={"arg": 1}, finalizer=finalizer,
                  final_args=(3, 4), max_tasks_per_worker=None)
# submit a task
future = pool.submit(add, 10, 2)

# test the pool
try:
  pool.test()
# exception coming from the initializer
except InitializerError as e:
  e.__cause__  # the cause
# exception coming from the finalizer
except FinalizerError:
  pass
# exception coming from the initializer
# or the finalizer
except BrokenPoolError:
  pass

# calling this will raise RuntimeError if the pool is closed
# or BrokenPoolError (or its subclass)
pool.check()

# retrieve useful data
pool.count_workers()
pool.count_busy_workers()
pool.count_free_workers()
pool.count_pending_tasks()

# manually spawn workers
pool.spawn_workers(2)  # 2 extra workers
# join all workers
pool.join(timeout=42)

# gracefully shut down the pool
pool.shutdown()
assert pool.is_terminated
# list of cancelled tasks
pool.cancelled_tasks
```

> Check out the API reference for [asyncpal.ThreadPool](https://github.com/pyrustic/asyncpal/blob/master/docs/api/modules/asyncpal/__init__/class-ThreadPool.md).

## ProcessPool class
Parallelism is achieved with the `ProcessPool` class. Under the hood, the process pool spawns Python's `multiprocessing.Process` as workers with the `spawn` context. 

The `ProcessPool` class is similar to the `ThreadPool` class. 

For convenience, the following four derived classes are provided:

- `SingleProcessPool`: spawns only 1 worker
- `DualProcessPool`: spawns up to 2 workers
- `TripleProcessPool`: spawns up to 3 workers
- `QuadProcessPool`: spawns up to 4 workers


> Note that you must guard your process pool with `if __name__ == '__main__'` and also avoid writting multiprocessing code directly in the `__main__` module of your projects.

> Check out the API reference for [asyncpal.ProcessPool](https://github.com/pyrustic/asyncpal/blob/master/docs/api/modules/asyncpal/__init__/class-ProcessPool.md).

## Future class

A [Future](https://en.wikipedia.org/wiki/Futures_and_promises) object is not meant to be instantiated by the programmer but rather returned by the `submit` method of pools.

```python
from asyncpal import ThreadPool


def divide(x, y):
  return x // y


with ThreadPool(4) as pool:
  # submit a task
  future = pool.submit(divide, 10, 2)

  # add a callback that accepts the future as argument
  # and that will be called when the future is done
  future.add_callback(lambda f: None)

  # safely collect the result (by default, it blocks)
  try:
    # blocks (max 42s) until the Future is done
    result = future.collect(timeout=42)
  except ZeroDivisionError as e:
    pass
  else:
    assert result == 5

  # get duration (in seconds)
  pending_time, running_time = future.duration

  # cancel the future (it is a bit too late, but ok)
  future.cancel()

  # we could've waited for the Future to be done (it blocks)
  future.wait(timeout=42)  # 42s !

  # get the result (returns None if the Future isn't done)
  result = future.result
  # get the exception (returns None if the Future isn't done)
  exc = future.exception

  # some useful properties
  future.cancel_flag  # boolean set to True after cancel() is called
  future.is_cancelled # boolean that confirms cancellation
  future.is_done      # True when Completed, Cancelled, or Failed
  future.is_pending   # True while task is pending
  future.is_running   # True while task is running
  # etc...
```


> Check out the API reference for [asyncpal.Future](https://github.com/pyrustic/asyncpal/blob/master/docs/api/modules/asyncpal/__init__/class-Future.md).

## Miscellaneous functions and classes

> Check out the API reference for [asyncpal](https://github.com/pyrustic/asyncpal/blob/master/docs/api/modules/asyncpal/__init__/funcs.md).


# Testing and contributing
Feel free to **open an issue** to report a bug, suggest some changes, show some useful code snippets, or discuss anything related to this project. You can also directly email [me](https://pyrustic.github.io/#contact).

## Setup your development environment
Following are instructions to setup your development environment

```bash
# create and activate a virtual environmentb
python -m venv venv
source venv/bin/activate

# clone the project then change into its directory
git clone https://github.com/pyrustic/asyncpal.git
cd asyncpal

# install the package locally (editable mode)
pip install -e .

# run tests
python -m tests

# deactivate the virtual environment
deactivate
```

<p align="right"><a href="#readme">Back to top</a></p>

# Installation
**Asyncpal** is **cross-platform**. It is built on [Ubuntu](https://ubuntu.com/download/desktop) and should work on **Python 3.8** or **newer**.

## Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

## Install for the first time

```bash
pip install asyncpal
```

## Upgrade the package
```bash
pip install asyncpal --upgrade --upgrade-strategy eager
```

## Deactivate the virtual environment
```bash
deactivate
```

<p align="right"><a href="#readme">Back to top</a></p>

# About the author
Hello world, I'm Alex, a tech enthusiast ! Feel free to get in touch with [me](https://pyrustic.github.io/#contact) !

<br>
<br>
<br>

[Back to top](#readme)


