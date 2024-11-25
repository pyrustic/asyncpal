import unittest
import time
from asyncpal import ThreadPool, errors, misc
from asyncpal.future import as_done, wait, collect, Future, FutureFilter
from tests import funcs


class TestResolveMethod(unittest.TestCase):

    def test_resolve_before_shutdown(self):
        with ThreadPool() as pool:
            future = pool.submit(funcs.add, 1, 2)
            self.assertEqual(3, future.collect())

    def test_resolve_after_shutdown(self):
        with ThreadPool() as pool:
            future = pool.submit(funcs.add, a=1, b=2)
        self.assertEqual(3, future.collect())

    def test_resolve_with_pool_broken_by_initializer(self):
        with ThreadPool(initializer=funcs.divide, init_args=(1, 0)) as pool:
            future = pool.submit(funcs.add, 1, 2)
            with self.assertRaises(errors.CancelledError):
                future.collect()

    def test_resolve_with_pool_broken_by_finalizer(self):
        with ThreadPool(finalizer=funcs.divide, final_args=(1, 0)) as pool:
            future = pool.submit(funcs.add, 1, 2)
            self.assertEqual(3, future.collect())
        self.assertTrue(True)

    def test_resolve_with_timeout(self):
        with ThreadPool() as pool:
            future = pool.submit(funcs.add, a=1, b=2)
            self.assertEqual(3, future.collect(timeout=3))

    def test_resolve_with_too_short_timeout(self):
        with ThreadPool() as pool:
            future = pool.submit(funcs.add, a=1, b=2, sleep=0.1)
            with self.assertRaises(TimeoutError):
                future.collect(timeout=0)  # 0 is The too short timeout ;)

    def test_resolve_with_task_exception(self):
        with ThreadPool(initializer=funcs.divide, init_args=(1, 0)) as pool:
            future = pool.submit(funcs.divide, 1, 0)
            with self.assertRaises(errors.CancelledError):
                future.collect()


class TestWaitMethod(unittest.TestCase):

    def test_wait_before_shutdown(self):
        with ThreadPool() as pool:
            future = pool.submit(funcs.add, 1, 2)
            self.assertTrue(future.wait())

    def test_wait_after_shutdown(self):
        with ThreadPool() as pool:
            future = pool.submit(funcs.add, a=1, b=2)
            self.assertTrue(future.wait())

    def test_wait_with_pool_broken_by_initializer(self):
        with ThreadPool(initializer=funcs.divide, init_args=(1, 0)) as pool:
            future = pool.submit(funcs.add, 1, 2)
            self.assertTrue(future.wait())

    def test_wait_with_pool_broken_by_finalizer(self):
        with ThreadPool(finalizer=funcs.divide, final_args=(1, 0)) as pool:
            future = pool.submit(funcs.add, 1, 2)
            self.assertTrue(future.wait())

    def test_wait_with_timeout(self):
        with ThreadPool() as pool:
            future = pool.submit(funcs.add, a=1, b=2)
            self.assertTrue(future.wait(timeout=3))

    def test_wait_with_too_short_timeout(self):
        with ThreadPool() as pool:
            future = pool.submit(funcs.add, a=1, b=2, sleep=0.1)
            self.assertFalse(future.wait(timeout=0))  # 0 is The too short timeout ;)

    def test_wait_with_task_exception(self):
        with ThreadPool(initializer=funcs.divide, init_args=(1, 0)) as pool:
            future = pool.submit(funcs.divide, 1, 0)
            future.wait()
        self.assertTrue(True)


class TestCancelMethod(unittest.TestCase):

    def test(self):
        with ThreadPool(max_workers=1) as pool:
            future_1 = pool.submit(funcs.add, 1, 2, sleep=0.1)
            future_2 = pool.submit(funcs.add, 3, 4)
            time.sleep(0.001)
            future_1.cancel()
            future_2.cancel()
        self.assertFalse(future_1.is_cancelled)
        self.assertTrue(future_2.is_cancelled)


class TestCallbacks(unittest.TestCase):

    def test_callbacks_property(self):
        with ThreadPool() as pool:
            future = pool.submit(funcs.add, 1, 2)
            future.add_callbacks((dummy_callback_1, dummy_callback_2,
                                  dummy_callback_3))
            future.remove_callback(dummy_callback_3)
        expected = (dummy_callback_1, dummy_callback_2)
        self.assertEqual(expected, future.callbacks)

    def test_add_callback_early(self):
        cache = list()
        with ThreadPool() as pool:
            future = pool.submit(funcs.add, 1, 2, sleep=0.1)
            future.add_callback(cache.append)
            future.add_callback(cache.append)
            future.add_callbacks((cache.append, cache.append))
        expected = [future for _ in range(4)]
        self.assertEqual(expected, cache)

    def test_add_callback_late(self):
        cache = list()
        with ThreadPool() as pool:
            future = pool.submit(funcs.add, 1, 2)
            future.collect()
        future.add_callback(cache.append)
        future.add_callback(cache.append)
        future.add_callbacks((cache.append, cache.append))
        expected = [future for _ in range(4)]
        self.assertEqual(expected, cache)

    def test_remove_callback(self):
        cache = list()
        with ThreadPool() as pool:
            future = pool.submit(funcs.add, 1, 2, sleep=0.1)
            # add callback
            future.add_callbacks((cache.append,
                                 cache.append,
                                 dummy_callback_1,
                                 dummy_callback_2,
                                 lambda f: cache.append(f)))
            # remove callbacks
            future.remove_callback(cache.append)
            future.remove_callbacks((dummy_callback_1,
                                    dummy_callback_2))
        expected = [future]
        self.assertEqual(expected, cache)


class TestProperties(unittest.TestCase):

    def test_pool_property(self):
        with ThreadPool() as pool:
            future = pool.submit(funcs.add, 1, 2)
            self.assertIs(pool, future.pool)

    def test_task_id_property(self):
        with ThreadPool() as pool:
            future_1 = pool.submit(funcs.add, 1, 2)
            future_2 = pool.submit(funcs.add, 1, 2)
            self.assertEqual(1, future_1.task_id)
            self.assertEqual(2, future_2.task_id)

    def test_pending_property(self):
        with ThreadPool(max_workers=1) as pool:
            future_1 = pool.submit(funcs.add, 1, 2, sleep=0.1)
            future_2 = pool.submit(funcs.add, 1, 2)
            future_3 = pool.submit(funcs.add, 1, 2)
            self.assertFalse(future_1.is_pending)
            self.assertTrue(future_2.is_pending)
            self.assertTrue(future_3.is_pending)
        self.assertFalse(future_1.is_pending)
        self.assertFalse(future_2.is_pending)
        self.assertFalse(future_3.is_pending)

    def test_running_property(self):
        with ThreadPool(max_workers=1) as pool:
            future_1 = pool.submit(funcs.add, 1, 2, sleep=0.1)
            future_2 = pool.submit(funcs.add, 1, 2)
            future_3 = pool.submit(funcs.add, 1, 2)
            self.assertTrue(future_1.is_running)
            self.assertFalse(future_2.is_running)
            self.assertFalse(future_3.is_running)
        self.assertFalse(future_1.is_running)
        self.assertFalse(future_2.is_running)
        self.assertFalse(future_3.is_running)

    def test_completed_property(self):
        with ThreadPool(max_workers=1) as pool:
            future_1 = pool.submit(funcs.add, 1, 2, sleep=0.1)
            future_2 = pool.submit(funcs.add, 1, 2)
            future_3 = pool.submit(funcs.add, 1, 2)
            self.assertFalse(future_1.is_completed)
            self.assertFalse(future_2.is_completed)
            self.assertFalse(future_3.is_completed)
            future_1.wait()
            future_2.wait()
            future_3.wait()
        self.assertTrue(future_1.is_completed)
        self.assertTrue(future_2.is_completed)
        self.assertTrue(future_3.is_completed)

    def test_failed_property(self):
        with ThreadPool(max_workers=1) as pool:
            future_1 = pool.submit(funcs.divide, 1, 0, sleep=0.1)
            self.assertFalse(future_1.is_failed)
            future_1.wait()
            self.assertTrue(future_1.is_failed)

    def test_cancelled_property(self):
        with ThreadPool(max_workers=1) as pool:
            future_1 = pool.submit(funcs.add, 1, 2, sleep=0.1)
            future_2 = pool.submit(funcs.add, 1, 2)
            self.assertFalse(future_1.is_cancelled)
            self.assertFalse(future_2.is_cancelled)
        self.assertFalse(future_1.is_cancelled)
        self.assertTrue(future_2.is_cancelled)  # task_2 got cancelled as the pool shut down...

    def test_cancel_flag(self):
        with ThreadPool(max_workers=1) as pool:
            future = pool.submit(funcs.add, 1, 2)
            future.cancel()
            self.assertTrue(future.cancel_flag)

    def test_done_property(self):
        with ThreadPool(max_workers=1) as pool:
            future_1 = pool.submit(funcs.divide, 1, 0)  # ZeroDivisionError !
            future_2 = pool.submit(funcs.add, 1, 2)
            time.sleep(0.1)
            future_3 = pool.submit(funcs.add, 1, 2)
            self.assertTrue(future_1.is_done)
            self.assertTrue(future_2.is_done)
            self.assertFalse(future_3.is_done)
        # failed (ZeroDivisionError), yet done
        self.assertTrue(future_1.is_failed)
        self.assertTrue(future_1.is_done)
        # completed, yet done
        self.assertTrue(future_2.is_completed)
        self.assertTrue(future_2.is_done)
        # cancelled (pool had to shut down quick), yet done
        self.assertTrue(future_3.is_cancelled)
        self.assertTrue(future_3.is_done)

    def test_result_property(self):
        with ThreadPool(max_workers=1) as pool:
            future_1 = pool.submit(funcs.divide, 1, 0)  # ZeroDivisionError !
            future_2 = pool.submit(funcs.add, 1, 2)
            time.sleep(0.1)
            future_3 = pool.submit(funcs.add, 1, 2)
            self.assertIsNone(future_1.result)
            self.assertEqual(3, future_2.result)
            self.assertIsNone(future_3.result)
        self.assertIsNone(future_1.result)
        self.assertEqual(3, future_2.result)
        self.assertIsNone(future_3.result)

    def test_exception_property(self):
        with ThreadPool(max_workers=1) as pool:
            future_1 = pool.submit(funcs.divide, 1, 0)  # ZeroDivisionError !
            future_2 = pool.submit(funcs.add, 1, 2)
            time.sleep(0.1)
            future_3 = pool.submit(funcs.add, 1, 2)
            self.assertIsInstance(future_1.exception, ZeroDivisionError)
            self.assertIsNone(future_2.exception)
            self.assertIsNone(future_3.exception)
        self.assertIsNone(future_2.exception)
        self.assertIsNone(future_3.exception)


class TestTaskDuration(unittest.TestCase):

    def test_with_pending_task(self):
        with ThreadPool() as pool:
            future = pool.submit(funcs.add, 1, 2, sleep=0.1)
            pending_duration, task_duration = future.duration
            self.assertEqual(0, pending_duration)
            self.assertEqual(0, task_duration)

    def test_with_completed_task(self):
        with ThreadPool() as pool:
            future = pool.submit(funcs.add, 1, 2)
            future.collect()
        pending_duration, task_duration = future.duration
        self.assertGreater(pending_duration, 0)
        self.assertGreater(task_duration, 0)

    def test_with_failed_task(self):
        with ThreadPool() as pool:
            future = pool.submit(funcs.divide, 1, 0)
            future.wait()
        pending_duration, task_duration = future.duration
        self.assertGreater(pending_duration, 0)
        self.assertGreater(task_duration, 0)

    def test_with_cancelled_task(self):
        with ThreadPool(max_workers=1) as pool:
            pool.submit(funcs.add, 1, 2, sleep=0.1)
            future = pool.submit(funcs.add, 1, 2)
        pending_duration, task_duration = future.duration
        self.assertGreater(pending_duration, 0)
        self.assertEqual(task_duration, 0)


class TestAsDoneFunction(unittest.TestCase):

    def test_with_order_maintained(self):
        with ThreadPool(max_workers=4) as pool:
            future_1 = pool.submit(funcs.add, 0, 1, sleep=0.1)
            future_2 = pool.submit(funcs.add, 1, 2)
            future_3 = pool.submit(funcs.add, 2, 3)
            futures = (future_1, future_2, future_3)
            it = as_done(futures, keep_order=True)  # keep_order defaults to False
            r = [future.collect() for future in it]
            expected = [1, 3, 5]
            self.assertEqual(expected, r)

    def test_without_order_maintained(self):
        with ThreadPool(max_workers=4) as pool:
            future_1 = pool.submit(funcs.add, 0, 1, sleep=0.5)
            future_2 = pool.submit(funcs.add, 1, 2, sleep=0.1)
            future_3 = pool.submit(funcs.add, 2, 3)
            futures = (future_1, future_2, future_3)
            it = as_done(futures, keep_order=False)  # keep_order defaults to False
            r = [future.collect() for future in it]
            expected = [5, 3, 1]
            self.assertEqual(expected, r)

    def test_with_unexpired_timeout(self):
        with ThreadPool(max_workers=4) as pool:
            future_1 = pool.submit(funcs.add, 0, 1, sleep=0.1)
            future_2 = pool.submit(funcs.add, 1, 2)
            future_3 = pool.submit(funcs.add, 2, 3)
            futures = (future_1, future_2, future_3)
            it = as_done(futures, keep_order=True, timeout=1)
            r = [future.collect() for future in it]
            expected = [1, 3, 5]
            self.assertEqual(expected, r)

    def test_with_expired_timeout(self):
        with ThreadPool(max_workers=1) as pool:
            future_1 = pool.submit(funcs.add, 0, 1, sleep=0.1)
            future_2 = pool.submit(funcs.add, 1, 2, sleep=0.1)
            future_3 = pool.submit(funcs.add, 2, 3, sleep=0.1)
            futures = (future_1, future_2, future_3)
            with self.assertRaises(TimeoutError):
                tuple(as_done(futures, keep_order=True, timeout=0.05))


class TestWaitFunction(unittest.TestCase):

    def test_wait_without_timeout(self):
        with ThreadPool() as pool:
            future_1 = pool.submit(funcs.add, 1, 2)
            future_2 = pool.submit(funcs.add, 3, 4)
            futures = (future_1, future_2)
            r = wait(futures)  # timeout defaults to None
            self.assertTrue(r)

    def test_wait_with_expired_timeout(self):
        with ThreadPool(max_workers=1) as pool:
            future_1 = pool.submit(funcs.add, 1, 2, sleep=0.1)
            future_2 = pool.submit(funcs.add, 3, 4, sleep=0.1)
            futures = (future_1, future_2)
            r = wait(futures, timeout=0.1)
            self.assertFalse(r)

    def test_wait_with_unexpired_timeout(self):
        with ThreadPool(max_workers=1) as pool:
            future_1 = pool.submit(funcs.add, 1, 2, sleep=0.1)
            future_2 = pool.submit(funcs.add, 3, 4, sleep=0.1)
            futures = (future_1, future_2)
            r = wait(futures, timeout=5)
            self.assertTrue(r)


class TestResolveFunction(unittest.TestCase):

    def test_resolve_without_exception(self):
        with ThreadPool() as pool:
            future_1 = pool.submit(funcs.add, 1, 2)
            future_2 = pool.submit(funcs.add, 3, 4)
            futures = (future_1, future_2)
            r = collect(futures)
            expected = (3, 7)
            self.assertEqual(expected, r)

    def test_resolve_with_exception(self):
        with ThreadPool() as pool:
            future_1 = pool.submit(funcs.divide, 2, 1)
            future_2 = pool.submit(funcs.divide, 1, 0)
            futures = (future_1, future_2)
            with self.assertRaises(ZeroDivisionError):
                collect(futures)

    def test_resolve_with_expired_timeout(self):
        with ThreadPool(max_workers=1) as pool:
            future_1 = pool.submit(funcs.add, 1, 2, sleep=0.1)
            future_2 = pool.submit(funcs.add, 3, 4, sleep=0.1)
            futures = (future_1, future_2)
            with self.assertRaises(TimeoutError):
                collect(futures, timeout=0.1)

    def test_resolve_with_unexpired_timeout(self):
        with ThreadPool(max_workers=1) as pool:
            future_1 = pool.submit(funcs.add, 1, 2, sleep=0.1)
            future_2 = pool.submit(funcs.add, 3, 4, sleep=0.1)
            futures = (future_1, future_2)
            r = collect(futures, timeout=5)
            expected = (3, 7)
            self.assertEqual(expected, r)


class TestFuture(unittest.TestCase):
    # Note that the Future class is already indirectly
    # tested throughout other tests

    def test(self):
        with ThreadPool() as pool:
            future = Future(pool, 1)
            future.set_result(42)
            self.assertIs(pool, future.pool)
            self.assertEqual(1, future.task_id)
            self.assertEqual(42, future.collect())


class TestFutureFilter(unittest.TestCase):

    def test_put_method(self):
        with ThreadPool(max_workers=4) as pool:
            future_1 = pool.submit(funcs.add, 0, 1, sleep=0.5)
            future_2 = pool.submit(funcs.add, 1, 2, sleep=0.1)
            future_3 = pool.submit(funcs.add, 2, 3)
            future_filter = FutureFilter()
            future_filter.put(future_1)
            future_filter.put(future_2)
            future_filter.put(future_3)
            r = drain_future_filter(future_filter)
            expected = [5, 3, 1]
            self.assertEqual(expected, r)

    def test_populate_method(self):
        with ThreadPool(max_workers=4) as pool:
            future_1 = pool.submit(funcs.add, 0, 1, sleep=0.5)
            future_2 = pool.submit(funcs.add, 1, 2, sleep=0.1)
            future_3 = pool.submit(funcs.add, 2, 3)
            future_filter = FutureFilter()
            future_filter.populate((future_1, future_2, future_3))
            r = drain_future_filter(future_filter)
            expected = [5, 3, 1]
            self.assertEqual(expected, r)

    def test_get_method_with_blocking(self):
        with ThreadPool(max_workers=4) as pool:
            future_filter = FutureFilter()
            with self.subTest():
                self.assertIsNone(future_filter.get(block=True))  # blocks by default
            with self.subTest():
                future = pool.submit(funcs.add, 0, 1)
                future_filter.put(future)
                f = future_filter.get(block=True)
                self.assertEqual(1, f.collect())
            with self.subTest():
                future = pool.submit(funcs.add, 1, 2, sleep=0.1)
                future_filter.put(future)
                # note that FutureFilter.get blocks by default
                # (block=True, timeout=None)
                f = future_filter.get(block=True)
                expected = 3
                self.assertEqual(expected, f.collect())

    def test_get_method_without_blocking(self):
        with ThreadPool(max_workers=4) as pool:
            future_filter = FutureFilter()
            with self.subTest():
                self.assertIsNone(future_filter.get(block=False))
            with self.subTest():
                future = pool.submit(funcs.add, 0, 1)
                future_filter.put(future)
                f = future_filter.get(block=False)
                self.assertEqual(1, f.collect())
            with self.subTest():
                future = pool.submit(funcs.add, 1, 2, sleep=0.1)
                future_filter.put(future)
                f = future_filter.get(block=False)
                self.assertIsNone(f)

    def test_get_method_without_timeout(self):
        with ThreadPool(max_workers=4) as pool:
            future_1 = pool.submit(funcs.add, 0, 1, sleep=0.5)
            future_2 = pool.submit(funcs.add, 1, 2, sleep=0.1)
            future_3 = pool.submit(funcs.add, 2, 3)
            futures = (future_1, future_2, future_3)
            future_filter = FutureFilter(futures)
            r = drain_future_filter(future_filter)
            expected = [5, 3, 1]
            self.assertEqual(expected, r)

    def test_get_method_with_expired_timeout(self):
        with ThreadPool(max_workers=4) as pool:
            future_1 = pool.submit(funcs.add, 0, 1, sleep=0.5)
            future_2 = pool.submit(funcs.add, 1, 2, sleep=0.1)
            future_3 = pool.submit(funcs.add, 2, 3)
            futures = (future_1, future_2, future_3)
            future_filter = FutureFilter(futures)
            with self.assertRaises(TimeoutError):
                drain_future_filter(future_filter, timeout=0.02)

    def test_get_method_with_unexpired_timeout(self):
        with ThreadPool(max_workers=4) as pool:
            future_1 = pool.submit(funcs.add, 0, 1, sleep=0.5)
            future_2 = pool.submit(funcs.add, 1, 2, sleep=0.1)
            future_3 = pool.submit(funcs.add, 2, 3)
            futures = (future_1, future_2, future_3)
            future_filter = FutureFilter(futures)
            r = drain_future_filter(future_filter, timeout=1)
            expected = [5, 3, 1]
            self.assertEqual(expected, r)

    def test_get_all_method_without_timeout(self):
        with ThreadPool(max_workers=4) as pool:
            future_1 = pool.submit(funcs.add, 0, 1, sleep=0.5)
            future_2 = pool.submit(funcs.add, 1, 2, sleep=0.1)
            future_3 = pool.submit(funcs.add, 2, 3)
            futures = (future_1, future_2, future_3)
            future_filter = FutureFilter(futures)
            r = [future.collect() for future in future_filter.get_all()]
            expected = [5, 3, 1]
            self.assertEqual(expected, r)

    def test_get_all_method_with_expired_timeout(self):
        with ThreadPool(max_workers=4) as pool:
            future_1 = pool.submit(funcs.add, 0, 1, sleep=0.5)
            future_2 = pool.submit(funcs.add, 1, 2, sleep=0.1)
            future_3 = pool.submit(funcs.add, 2, 3)
            futures = (future_1, future_2, future_3)
            future_filter = FutureFilter(futures)
            with self.assertRaises(TimeoutError):
                [future.collect() for future
                 in future_filter.get_all(timeout=0.02)]

    def test_get_all_method_with_unexpired_timeout(self):
        with ThreadPool(max_workers=4) as pool:
            future_1 = pool.submit(funcs.add, 0, 1, sleep=0.5)
            future_2 = pool.submit(funcs.add, 1, 2, sleep=0.1)
            future_3 = pool.submit(funcs.add, 2, 3)
            futures = (future_1, future_2, future_3)
            future_filter = FutureFilter(futures)
            r = [future.collect() for future
                 in future_filter.get_all(timeout=1)]
            expected = [5, 3, 1]
            self.assertEqual(expected, r)


def dummy_callback_1(future):
    pass


def dummy_callback_2(future):
    pass


def dummy_callback_3(future):
    pass


def drain_future_filter(future_filter, block=True, timeout=None):
    countdown = misc.Countdown(timeout)
    n = len(future_filter.futures)
    result = list()
    for _ in range(n):
        new_timeout = countdown.check()
        future = future_filter.get(block=block, timeout=new_timeout)
        result.append(future.collect())
    return result


if __name__ == "__main__":
    unittest.main()
