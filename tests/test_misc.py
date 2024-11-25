import os
import sys
import unittest
import time
import itertools
from traceback import format_exception
from queue import Queue
from asyncpal import misc, errors
from asyncpal.pool import MP_CONTEXT
from tests import funcs


class TestGetChunksFunction(unittest.TestCase):

    def test_with_empty_iterable(self):
        r = tuple(misc.get_chunks(list(), chunk_size=1))
        self.assertEqual(tuple(), r)

    def test_with_chunk_size_equals_1(self):
        i = 0
        for chunk in misc.get_chunks([0, 1, 2, 3], chunk_size=1):
            with self.subTest(i):
                self.assertEqual(1, len(chunk))
                self.assertEqual(i, chunk[0])
            i += 1

    def test_with_chunk_size_equals_2(self):
        i = 0
        for chunk in misc.get_chunks([0, 1, 2, 3], chunk_size=2):
            with self.subTest(i):
                self.assertEqual(2, len(chunk))
                self.assertEqual(i, chunk[0])
                self.assertEqual(i+1, chunk[1])
            i += 2

    def test_with_chunk_size_equals_3(self):
        i = 0
        for chunk in misc.get_chunks([0, 1, 2, 3, 4, 5], chunk_size=3):
            with self.subTest(i):
                self.assertEqual(3, len(chunk))
                self.assertEqual(i, chunk[0])
                self.assertEqual(i+1, chunk[1])
                self.assertEqual(i+2, chunk[2])
            i += 3

    def test_with_too_big_chunk_size(self):
        i = 0
        for chunk in misc.get_chunks([0, 1, 2], chunk_size=5):
            with self.subTest(i):
                self.assertEqual(3, len(chunk))
                self.assertEqual((0, 1, 2), chunk)
                self.assertEqual(0, i)
            i += 1

    def test_with_odd_iterable_but_even_chunk_size(self):
        i = 0
        for chunk in misc.get_chunks([0, 1, 2], chunk_size=2):
            with self.subTest(i):
                if i == 0:
                    self.assertEqual((0, 1), chunk)
                elif i == 1:
                    self.assertEqual((2, ), chunk)
                else:
                    raise Exception
            i += 1


class TestEnsureArgsKwargs(unittest.TestCase):

    def test_without_arguments(self):
        r = misc.ensure_args_kwargs()
        expected = (tuple(), dict())
        self.assertEqual(expected, r)

    def test_with_args(self):
        r = misc.ensure_args_kwargs([0, 1], None)
        expected = ([0, 1], dict())
        self.assertEqual(expected, r)

    def test_with_kwargs(self):
        r = misc.ensure_args_kwargs(None, {"a": 0, "b": 1})
        expected = (tuple(), {"a": 0, "b": 1})
        self.assertEqual(expected, r)

    def test_with_args_and_kwargs(self):
        r = misc.ensure_args_kwargs([0, 1], {"a": 0, "b": 1})
        expected = ([0, 1], {"a": 0, "b": 1})
        self.assertEqual(expected, r)


class TestDrainQueue(unittest.TestCase):

    def test_drain_regular_queue(self):
        n = 10
        q = Queue()
        for x in range(n):
            q.put(x)
        self.assertEqual(n, q.qsize())
        misc.drain_queue(q)
        self.assertEqual(0, q.qsize())

    def test_drain_multiprocessing_queue(self):
        n = 10
        q = MP_CONTEXT.Queue()
        for x in range(n):
            q.put(x)
        time.sleep(0.01)  # give time to the background thread
        self.assertEqual(n, q.qsize())
        misc.drain_queue(q)
        time.sleep(0.01)
        self.assertEqual(0, q.qsize())


class TestIterateQueue(unittest.TestCase):

    def test_iterate_regular_queue(self):
        n = 10
        q = Queue()
        for x in range(n):
            q.put(x)
        r = tuple(misc.iterate_queue(q))
        self.assertEqual(tuple(range(n)), r)

    def test_iterate_multiprocessing_queue(self):
        n = 10
        q = MP_CONTEXT.Queue()
        for x in range(n):
            q.put(x)
        time.sleep(0.1)  # give time to the background thread
        r = tuple(misc.iterate_queue(q))
        self.assertEqual(tuple(range(n)), r)


class TestAddFunction(unittest.TestCase):

    def test(self):
        for x in range(10):
            with self.subTest(x):
                r = misc.add(x, x)
                self.assertEqual(x+x, r)


class TestCountdownClass(unittest.TestCase):

    def test_with_null_timeout(self):
        timeout = None
        timeout_updater = misc.Countdown(timeout)
        r = timeout_updater.check()
        self.assertIsNone(r)

    def test_with_zero_timeout(self):
        timeout = 0
        timeout_updater = misc.Countdown(timeout)
        r = timeout_updater.check()
        self.assertEqual(0, r)

    def test_with_expired_timeout(self):
        timeout = 0.01
        timeout_updater = misc.Countdown(timeout)
        time.sleep(0.01)
        r = timeout_updater.check()
        self.assertEqual(0, r)

    def test_with_unexpired_timeout(self):
        timeout = 0.01
        timeout_updater = misc.Countdown(timeout)
        r = timeout_updater.check()
        self.assertGreater(r, 0)


class TestSplitMapTask(unittest.TestCase):

    def test_without_chunk_size(self):
        result = list()
        subtasks = tuple(misc.split_map_task(funcs.square, range(10)))
        n = len(subtasks)
        for subtask in subtasks:
            result.extend(subtask())
        expected = tuple(map(funcs.square, range(10)))
        self.assertEqual(10, n)
        self.assertEqual(expected, tuple(result))

    def test_with_chunk_size(self):
        result = list()
        subtasks = tuple(misc.split_map_task(funcs.square, range(10),
                                             chunk_size=2))
        n = len(subtasks)
        for subtask in subtasks:
            result.extend(subtask())
        expected = tuple(map(funcs.square, range(10)))
        self.assertEqual(5, n)
        self.assertEqual(expected, tuple(result))


class TestSplitStarmapTask(unittest.TestCase):

    def test_without_chunk_size(self):
        result = list()
        it = zip(range(10), range(10))
        subtasks = tuple(misc.split_starmap_task(funcs.add, it))
        n = len(subtasks)
        for subtask in subtasks:
            result.extend(subtask())
        it = zip(range(10), range(10))
        expected = tuple(itertools.starmap(funcs.add, it))
        self.assertEqual(10, n)
        self.assertEqual(expected, tuple(result))

    def test_with_chunk_size(self):
        result = list()
        it = zip(range(10), range(10))
        subtasks = tuple(misc.split_starmap_task(funcs.add, it,
                                                 chunk_size=2))
        n = len(subtasks)
        for subtask in subtasks:
            result.extend(subtask())
        it = zip(range(10), range(10))
        expected = tuple(itertools.starmap(funcs.add, it))
        self.assertEqual(5, n)
        self.assertEqual(expected, tuple(result))


class TestCpuCount(unittest.TestCase):

    def test(self):
        if sys.version_info >= (3, 13):
            cpu_count = os.process_cpu_count()
        else:
            cpu_count = os.cpu_count()
        self.assertEqual(cpu_count, misc.get_cpu_count())


class TestFunctionGetRemoteTraceback(unittest.TestCase):

    def setUp(self):
        try:
            try:
                try:
                    try:
                        raise Exception("d")
                    except Exception as e:
                        raise Exception("c")
                except Exception as e:
                    raise Exception("b") from e
            except Exception as e:
                raise Exception("a") from e
        except Exception as e:
            self._exc = e
            self._exc_wrapper = misc.RemoteExceptionWrapper(e)

    def test(self):
        self.assertIsNone(misc.get_remote_traceback(self._exc))
        exc = self._exc_wrapper.unwrap()
        x = format_exception(type(self._exc), self._exc,
                             self._exc.__traceback__)
        x = "".join(x).strip()
        self.assertEqual(x, misc.get_remote_traceback(exc))


class TestRemoteExceptionWrapper(unittest.TestCase):

    def setUp(self):
        try:
            try:
                try:
                    try:
                        raise Exception("d")
                    except Exception as e:
                        raise Exception("c")
                except Exception as e:
                    raise Exception("b") from e
            except Exception as e:
                raise Exception("a") from e
        except Exception as e:
            self._exc = e
            self._exc_wrapper = misc.RemoteExceptionWrapper(e)

    def test_exc_chain_length(self):
        exc_chain = self._exc_wrapper.exc_chain
        self.assertEqual(4, len(exc_chain))

    def test_exc_chain(self):
        exc_chain = self._exc_wrapper.exc_chain
        exc_a, exc_a_has_cause = exc_chain[0]
        exc_b, exc_b_has_cause = exc_chain[1]
        exc_c, exc_c_has_cause = exc_chain[2]
        exc_d, exc_d_has_cause = exc_chain[3]
        self.assertEqual("a", str(exc_a))
        self.assertEqual("b", str(exc_b))
        self.assertEqual("c", str(exc_c))
        self.assertEqual("d", str(exc_d))
        self.assertTrue(exc_a_has_cause)
        self.assertTrue(exc_b_has_cause)
        self.assertFalse(exc_c_has_cause)
        self.assertFalse(exc_d_has_cause)

    def test_unwrap_method(self):
        exc = self._exc_wrapper.unwrap()
        self.assertEqual(str(self._exc), str(exc))
        self.assertEqual(str(self._exc.__cause__), str(exc.__cause__))
        self.assertEqual(str(self._exc.__cause__.__cause__), str(exc.__cause__.__cause__))
        self.assertEqual(str(self._exc.__cause__.__cause__.__context__),
                         str(exc.__cause__.__cause__.__context__))
        last_exc = exc.__cause__.__cause__.__context__
        self.assertIsInstance(last_exc.__context__, errors.RemoteTraceback)


if __name__ == "__main__":
    unittest.main()
