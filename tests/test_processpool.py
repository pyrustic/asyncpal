import unittest
import time
import itertools
from asyncpal import errors
from tests import funcs
from asyncpal import (ProcessPool, SingleProcessPool,
                      DualProcessPool, TripleProcessPool,
                      QuadProcessPool)


class TestWorkers(unittest.TestCase):

    def test_worker(self):
        with ProcessPool() as pool:
            pool.test()
        self.assertTrue(True)

    def test_worker_after_shutdown(self):
        with ProcessPool() as pool:
            pass
        with self.assertRaises(RuntimeError):
            pool.test()

    def test_worker_with_broken_pool(self):
        with ProcessPool(initializer=funcs.divide, init_args=(1, 0)) as pool:
            pool.spawn_workers(1)
            pool.join()
            with self.assertRaises(errors.BrokenPoolError):
                pool.test()
            worker_exception = funcs.get_worker_exception(pool)
            first_cause = worker_exception.__cause__
            self.assertIsInstance(first_cause, ZeroDivisionError)


class TestBrokenPool(unittest.TestCase):

    def test_before_shutdown_with_pool_broken_by_initializer(self):
        with ProcessPool(initializer=funcs.divide, init_args=(1, 0)) as pool:
            pool.spawn_workers(1)
            pool.join()
            with self.assertRaises(errors.InitializerError):
                pool.check()
            with self.assertRaises(errors.BrokenPoolError):
                pool.check()
            worker_exception = funcs.get_worker_exception(pool)
            self.assertIsInstance(worker_exception, errors.InitializerError)
            self.assertIsInstance(worker_exception, errors.BrokenPoolError)
            first_cause = worker_exception.__cause__
            self.assertIsInstance(first_cause, ZeroDivisionError)
            self.assertTrue(pool.is_broken)

    def test_after_shutdown_with_pool_broken_by_initializer(self):
        with ProcessPool(initializer=funcs.divide, init_args=(1, 0)) as pool:
            pool.spawn_workers(1)
            pool.join()
            with self.assertRaises(errors.InitializerError):
                pool.check()
            with self.assertRaises(errors.BrokenPoolError):
                pool.check()
        with self.assertRaises(RuntimeError):
            pool.check()

    def test_before_shutdown_with_pool_broken_by_finalizer(self):
        # idle_timeout is set to 0 so the worker will quickly
        # return, giving chance to finalizer to run before 'check()'
        with ProcessPool(finalizer=funcs.divide, final_args=(1, 0),
                         idle_timeout=0) as pool:
            pool.spawn_workers(1)
            pool.join()
            with self.assertRaises(errors.FinalizerError):
                pool.check()
            with self.assertRaises(errors.BrokenPoolError):
                pool.check()
            worker_exception = funcs.get_worker_exception(pool)
            self.assertIsInstance(worker_exception, errors.FinalizerError)
            self.assertIsInstance(worker_exception, errors.BrokenPoolError)
            first_cause = worker_exception.__cause__
            self.assertIsInstance(first_cause, ZeroDivisionError)
            self.assertTrue(pool.is_broken)

    def test_after_shutdown_with_pool_broken_by_finalizer(self):
        with ProcessPool(finalizer=funcs.divide, final_args=(1, 0)) as pool:
            pool.spawn_workers(1)
            pool.join()
            with self.assertRaises(errors.FinalizerError):
                pool.check()
            with self.assertRaises(errors.BrokenPoolError):
                pool.check()
        with self.assertRaises(RuntimeError):
            pool.check()

    def test_with_pool_broken_by_initializer_missing_args_error(self):
        with ProcessPool(initializer=funcs.divide) as pool:
            pool.spawn_workers(1)
            pool.join()
            worker_exception = funcs.get_worker_exception(pool)
            first_cause = worker_exception.__cause__
            self.assertIsInstance(first_cause, TypeError)
            self.assertTrue(pool.is_broken)


class TestCheckMethod(unittest.TestCase):

    def test_check_before_shutdown(self):
        with ProcessPool() as pool:
            pool.check()
        self.assertTrue(True)

    def test_check_after_shutdown(self):
        with ProcessPool() as pool:
            pass
        with self.assertRaises(RuntimeError):
            pool.check()

    def test_check_before_shutdown_with_pool_broken_by_initializer(self):
        with ProcessPool(initializer=funcs.divide, init_args=(1, 0), idle_timeout=1) as pool:
            with self.assertRaises(errors.CancelledError):
                # I could've put 'pool.spawn_workers(1)' here
                # but 'pool.check()' risks to complete before
                # the worker returns
                pool.submit(funcs.add, 1, 2).collect()
            with self.assertRaises(errors.InitializerError):
                pool.check()
            with self.assertRaises(errors.BrokenPoolError):
                pool.check()

    def test_check_after_shutdown_with_pool_broken_by_initializer(self):
        with ProcessPool(initializer=funcs.divide, init_args=(1, 0)) as pool:
            # I could've put 'pool.submit(funcs.add, 1, 2).resolve()' here
            # instead of 'pool.spawn_workers(1)', but it is not needed
            # as 'pool.check()' will be run after the shutdown of the pool,
            # which guarantees that the worker would've already returned.
            pool.spawn_workers(1)
        with self.assertRaises(RuntimeError):
            pool.check()

    def test_check_before_shutdown_with_pool_broken_by_finalizer(self):
        with ProcessPool(finalizer=funcs.divide, final_args=(1, 0)) as pool:
            pool.spawn_workers(1)
            pool.join()
            with self.assertRaises(errors.FinalizerError):
                pool.check()
            with self.assertRaises(errors.BrokenPoolError):
                pool.check()

    def test_check_after_shutdown_with_pool_broken_by_finalizer(self):
        with ProcessPool(finalizer=funcs.divide, final_args=(1, 0)) as pool:
            pool.spawn_workers(1)
        with self.assertRaises(RuntimeError):
            pool.check()


class TestRunMethod(unittest.TestCase):

    def test_submit_to_pool(self):
        with ProcessPool() as pool:
            r = pool.run(funcs.add, 1, 2)
            self.assertEqual(3, r)

    def test_submit_to_broken_pool(self):
        with ProcessPool(initializer=funcs.divide, init_args=(1, 0)) as pool:
            with self.assertRaises(errors.CancelledError):
                pool.run(funcs.add, 1, 2)

    def test_submit_to_closed_pool(self):
        with ProcessPool() as pool:
            pass
        with self.assertRaises(RuntimeError):
            pool.run(funcs.add, 1, 2)

    def test_submit_to_broken_and_closed_pool(self):
        with ProcessPool(initializer=funcs.divide, init_args=(1, 0)) as pool:
            pool.spawn_workers(1)
        with self.assertRaises(RuntimeError):
            pool.run(funcs.add, 1, 2)


class TestSubmitMethod(unittest.TestCase):

    def test_submit_to_pool(self):
        with ProcessPool() as pool:
            future = pool.submit(funcs.add, 1, 2)
            self.assertEqual(3, future.collect())

    def test_submit_to_broken_pool(self):
        with ProcessPool(initializer=funcs.divide, init_args=(1, 0)) as pool:
            future = pool.submit(funcs.add, 1, 2)
            with self.assertRaises(errors.CancelledError):
                future.collect()

    def test_submit_to_closed_pool(self):
        with ProcessPool() as pool:
            pass
        with self.assertRaises(RuntimeError):
            pool.submit(funcs.add, 1, 2)

    def test_submit_to_broken_and_closed_pool(self):
        with ProcessPool(initializer=funcs.divide, init_args=(1, 0)) as pool:
            pool.spawn_workers(1)
        with self.assertRaises(RuntimeError):
            pool.submit(funcs.add, 1, 2)


class TestProperties(unittest.TestCase):

    def test_closed_property(self):
        with ProcessPool() as pool:
            self.assertFalse(pool.is_closed)
        self.assertTrue(pool.is_closed)

    def test_terminated_property(self):
        with ProcessPool() as pool:
            self.assertFalse(pool.is_terminated)
        self.assertTrue(pool.is_terminated)

    def test_broken_property(self):
        with ProcessPool(initializer=funcs.divide, init_args=(1, 0)) as pool:
            self.assertFalse(pool.is_broken)
            pool.spawn_workers(1)
        self.assertTrue(pool.is_broken)


class TestLazyMapMethod(unittest.TestCase):

    def test_with_defaults(self):
        with ProcessPool(max_workers=4) as pool:
            r = tuple(pool.map(funcs.square, range(10)))
            expected = tuple(map(funcs.square, range(10)))
            self.assertEqual(expected, r)
            self.assertLessEqual(pool.count_workers(), 2)

    def test_with_custom_chunk_size(self):
        with ProcessPool(max_workers=4) as pool:
            r = tuple(pool.map(funcs.square, range(10), chunk_size=5))
            expected = tuple(map(funcs.square, range(10)))
            self.assertEqual(expected, r)
            self.assertLessEqual(pool.count_workers(), 2)

    def test_with_buffer_size(self):
        # as processes aren't as reactive as threads, one extra process
        # might be spawn, that's why instead of 3 (the buffer size),
        # I've put 4 in self.assertLessEqual(pool.count_workers(), 4)
        # and increased the max_workers from 4 to 7
        with ProcessPool(max_workers=7) as pool:
            r = tuple(pool.map(funcs.square, range(10), chunk_size=1,
                               buffer_size=3))
            expected = tuple(map(funcs.square, range(10)))
            self.assertEqual(expected, r)
            self.assertLessEqual(pool.count_workers(), 4)

    def test_with_unordered_result(self):
        with ProcessPool(max_workers=4) as pool:
            r = tuple(pool.map(funcs.square, range(3),
                               (0.5, 0.2, 0),
                               keep_order=False, buffer_size=3))
            expected = tuple(map(funcs.square, (2, 1, 0)))
            self.assertEqual(expected, r)
            self.assertLessEqual(pool.count_workers(), 3)

    def test_with_unexpired_timeout(self):
        with ProcessPool(max_workers=4) as pool:
            r = tuple(pool.map(funcs.square, range(10), timeout=1))
            expected = tuple(map(funcs.square, range(10)))
            self.assertEqual(expected, r)

    def test_with_expired_timeout(self):
        with ProcessPool(max_workers=4) as pool:
            with self.assertRaises(TimeoutError):
                tuple(pool.map(funcs.square,
                               range(5),  # square numbers from 0 to 4
                               [0.02 for _ in range(5)],  # sleep for 0.01 s
                               timeout=0.01))


class TestEagerMapMethod(unittest.TestCase):

    def test_with_defaults(self):
        with ProcessPool(max_workers=4) as pool:
            r = tuple(pool.map_all(funcs.square, range(10)))
            expected = tuple(map(funcs.square, range(10)))
            self.assertEqual(expected, r)
            self.assertEqual(4, pool.count_workers())

    def test_with_custom_chunk_size(self):
        with ProcessPool(max_workers=4) as pool:
            r = tuple(pool.map_all(funcs.square, range(10), chunk_size=5))
            expected = tuple(map(funcs.square, range(10)))
            self.assertEqual(expected, r)
            self.assertLessEqual(pool.count_workers(), 2)

    def test_with_unordered_result(self):
        with ProcessPool(max_workers=4) as pool:
            r = tuple(pool.map_all(funcs.square, range(3),
                                   (0.6, 0.3, 0),
                                   keep_order=False))
            expected = tuple(map(funcs.square, (2, 1, 0)))
            self.assertEqual(expected, r)
            self.assertLessEqual(pool.count_workers(), 3)

    def test_with_unexpired_timeout(self):
        with ProcessPool(max_workers=4) as pool:
            r = tuple(pool.map_all(funcs.square, range(10), timeout=5))
            expected = tuple(map(funcs.square, range(10)))
            self.assertEqual(expected, r)

    def test_with_expired_timeout(self):
        with ProcessPool(max_workers=4) as pool:
            with self.assertRaises(TimeoutError):
                tuple(pool.map_all(funcs.square,
                                   range(5),  # square numbers from 0 to 4
                                   [0.02 for _ in range(5)],  # sleep for 0.01 s
                                   timeout=0.01))


class TestLazyStarmapMethod(unittest.TestCase):

    def test_with_defaults(self):
        with ProcessPool(max_workers=4) as pool:
            r = tuple(pool.starmap(funcs.add, zip(range(10), range(10))))
            expected = tuple(itertools.starmap(funcs.add, zip(range(10), range(10))))
            self.assertEqual(expected, r)
            self.assertEqual(1, pool.count_workers())

    def test_with_custom_chunk_size(self):
        with ProcessPool(max_workers=4) as pool:
            r = tuple(pool.starmap(funcs.add, zip(range(10), range(10)), chunk_size=5))
            expected = tuple(itertools.starmap(funcs.add, zip(range(10), range(10))))
            self.assertEqual(expected, r)
            self.assertLessEqual(pool.count_workers(), 2)

    def test_with_buffer_size(self):
        # as processes aren't as reactive as threads, one extra process
        # might be spawn, that's why instead of 3 (the buffer size),
        # I've put 4 in self.assertLessEqual(pool.count_workers(), 4)
        # and increased the max_workers from 4 to 7
        with ProcessPool(max_workers=7) as pool:
            r = tuple(pool.starmap(funcs.add, zip(range(10), range(10)),
                                   chunk_size=1, buffer_size=3))
            expected = tuple(itertools.starmap(funcs.add, zip(range(10), range(10))))
            self.assertEqual(expected, r)
            self.assertLessEqual(pool.count_workers(), 4)

    def test_with_unordered_result(self):
        with ProcessPool(max_workers=4) as pool:
            r = tuple(pool.starmap(funcs.add, zip(range(3), range(3),
                                                  (0.5, 0.2, 0)),
                                   keep_order=False, buffer_size=3))
            expected = tuple(itertools.starmap(funcs.add,
                                               [(2, 2), (1, 1), (0, 0)]))
            self.assertEqual(expected, r)
            self.assertEqual(3, pool.count_workers())

    def test_with_unexpired_timeout(self):
        with ProcessPool(max_workers=4) as pool:
            r = tuple(pool.starmap(funcs.add, zip(range(10), range(10)), timeout=1))
            expected = tuple(itertools.starmap(funcs.add, zip(range(10), range(10))))
            self.assertEqual(expected, r)

    def test_with_expired_timeout(self):
        with ProcessPool(max_workers=4) as pool:
            with self.assertRaises(TimeoutError):
                tuple(pool.starmap(funcs.add,
                                   zip(range(5), range(5),
                                       [0.02 for _ in range(5)]),
                                   timeout=0.01))


class TestEagerStarmapMethod(unittest.TestCase):

    def test_with_defaults(self):
        with ProcessPool(max_workers=4) as pool:
            r = tuple(pool.starmap_all(funcs.add, zip(range(10), range(10))))
            expected = tuple(itertools.starmap(funcs.add, zip(range(10), range(10))))
            self.assertEqual(expected, r)
            self.assertEqual(4, pool.count_workers())

    def test_with_custom_chunk_size(self):
        with ProcessPool(max_workers=4) as pool:
            r = tuple(pool.starmap_all(funcs.add, zip(range(10), range(10)), chunk_size=5))
            expected = tuple(itertools.starmap(funcs.add, zip(range(10), range(10))))
            self.assertEqual(expected, r)
            self.assertLessEqual(pool.count_workers(), 2)

    def test_with_unordered_result(self):
        with ProcessPool(max_workers=4) as pool:
            r = tuple(pool.starmap_all(funcs.add, zip(range(3), range(3),
                                                      (0.5, 0.2, 0)),
                                       keep_order=False))
            expected = tuple(itertools.starmap(funcs.add,
                                               [(2, 2), (1, 1), (0, 0)]))
            self.assertEqual(expected, r)
            self.assertEqual(3, pool.count_workers())

    def test_with_unexpired_timeout(self):
        with ProcessPool(max_workers=4) as pool:
            r = tuple(pool.starmap_all(funcs.add, zip(range(10),
                                                      range(10)), timeout=1))
            expected = tuple(itertools.starmap(funcs.add,
                                               zip(range(10), range(10))))
            self.assertEqual(expected, r)

    def test_with_expired_timeout(self):
        with ProcessPool(max_workers=4) as pool:
            with self.assertRaises(TimeoutError):
                tuple(pool.starmap_all(funcs.add,
                                       zip(range(5), range(5),
                                           [0.02 for _ in range(5)]),
                                       timeout=0.01))


class TestSpawnWorkersMethod(unittest.TestCase):

    def test(self):
        with ProcessPool(max_workers=4) as pool:
            self.assertEqual(0, pool.count_workers())
            pool.spawn_workers(3)
            self.assertEqual(3, pool.count_workers())


class TestCountWorkersMethod(unittest.TestCase):

    def test(self):
        with ProcessPool(max_workers=4) as pool:
            self.assertEqual(0, pool.count_workers())
            pool.spawn_workers(1)
            self.assertEqual(1, pool.count_workers())
            pool.join()
            self.assertEqual(0, pool.count_workers())


class TestCountBusyWorkersMethod(unittest.TestCase):

    def test(self):
        with ProcessPool(max_workers=1) as pool:
            self.assertEqual(0, pool.count_busy_workers())
            pool.submit(funcs.add, 1, 2, sleep=1)
            time.sleep(0.5)
            self.assertEqual(1, pool.count_busy_workers())
            pool.join()
            self.assertEqual(0, pool.count_busy_workers())


class TestCountPendingTasksMethod(unittest.TestCase):

    def test(self):
        with ProcessPool(max_workers=1) as pool:
            self.assertEqual(0, pool.count_pending_tasks())
            pool.submit(funcs.add, 1, 2, sleep=0.01)
            pool.submit(funcs.add, 1, 2)
            pool.submit(funcs.add, 1, 2)
            self.assertLessEqual(pool.count_pending_tasks(), 3)


class TestCancelledTasksProperty(unittest.TestCase):

    def test(self):
        with ProcessPool(max_workers=1) as pool:
            self.assertEqual(0, len(pool.cancelled_tasks))
            pool.submit(funcs.add, 1, 2, sleep=0.01)
            pool.submit(funcs.add, 1, 2)  # will be cancelled soon
            pool.submit(funcs.add, 1, 2)  # will be cancelled soon
        self.assertLessEqual(len(pool.cancelled_tasks), 3)


class TestSpawnMaxWorkers(unittest.TestCase):

    def test(self):
        with ProcessPool(max_workers=4) as pool:
            self.assertEqual(0, pool.count_workers())
            pool.spawn_max_workers()
            self.assertEqual(4, pool.count_workers())
        self.assertEqual(0, pool.count_workers())


class TestJoinPool(unittest.TestCase):

    def test_join(self):
        with ProcessPool(max_workers=1, idle_timeout=60) as pool:
            instant_a = time.monotonic()
            pool.spawn_workers(1)
            self.assertTrue(pool.join())
            # t should be <= 1 second
            # despite the 60 seconds idle_timeout
            t = time.monotonic() - instant_a
            self.assertLessEqual(t, 1)

    def test_join_with_unexpired_timeout(self):
        with ProcessPool(max_workers=1) as pool:
            future_1 = pool.submit(funcs.add, 1, 2, sleep=0.01)
            future_2 = pool.submit(funcs.add, 3, 4, sleep=0.01)
            self.assertTrue(pool.join(5))
            self.assertTrue(3, future_1.result)
            self.assertTrue(7, future_2.result)

    def test_join_with_expired_timeout(self):
        with ProcessPool(max_workers=1) as pool:
            future_1 = pool.submit(funcs.add, 1, 2, sleep=0.01)
            future_2 = pool.submit(funcs.add, 3, 4, sleep=0.01)
            self.assertFalse(pool.join(0.01))
            self.assertTrue(3, future_1.result)
            self.assertIsNone(future_2.result)


class TestMaxTasksByWorker(unittest.TestCase):

    def test(self):
        with ProcessPool(max_workers=1, max_tasks_per_worker=3, idle_timeout=60) as pool:
            pool.run(funcs.add, 1, 2)
            pool.run(funcs.add, 3, 4)
            pool.run(funcs.add, 5, 6)
            time.sleep(0.01)
            self.assertEqual(0, pool.count_workers())


class TestSizedPools(unittest.TestCase):

    def test_single_process_pool(self):
        with SingleProcessPool() as pool:
            self.assertEqual(0, pool.count_workers())
            pool.spawn_max_workers()
            self.assertEqual(1, pool.count_workers())
        self.assertEqual(0, pool.count_workers())

    def test_dual_process_pool(self):
        with DualProcessPool() as pool:
            self.assertEqual(0, pool.count_workers())
            pool.spawn_max_workers()
            self.assertEqual(2, pool.count_workers())
        self.assertEqual(0, pool.count_workers())

    def test_triple_process_pool(self):
        with TripleProcessPool() as pool:
            self.assertEqual(0, pool.count_workers())
            pool.spawn_max_workers()
            self.assertEqual(3, pool.count_workers())
        self.assertEqual(0, pool.count_workers())

    def test_quad_process_pool(self):
        with QuadProcessPool() as pool:
            self.assertEqual(0, pool.count_workers())
            pool.spawn_max_workers()
            self.assertEqual(4, pool.count_workers())
        self.assertEqual(0, pool.count_workers())
        
        
if __name__ == "__main__":
    unittest.main()
