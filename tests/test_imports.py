import unittest


class TestImports(unittest.TestCase):

    def test_import_classes(self):
        try:
            # import classes
            from asyncpal import Pool
            from asyncpal import ThreadPool
            from asyncpal import ProcessPool
            from asyncpal import SingleThreadPool
            from asyncpal import SingleProcessPool
            from asyncpal import DualThreadPool
            from asyncpal import DualProcessPool
            from asyncpal import TripleThreadPool
            from asyncpal import TripleProcessPool
            from asyncpal import QuadThreadPool
            from asyncpal import QuadProcessPool
            from asyncpal import Future
            from asyncpal import FutureFilter
            from asyncpal import Countdown
            # import functions
            from asyncpal import as_done
            from asyncpal import wait
            from asyncpal import collect
            from asyncpal import split_map_task
            from asyncpal import split_starmap_task
            from asyncpal import get_chunks
            from asyncpal import get_remote_traceback
            # import constants
            from asyncpal import IDLE_TIMEOUT
            from asyncpal import MP_CONTEXT
            from asyncpal import LOGGER
            from asyncpal import WINDOWS_MAX_PROCESS_WORKERS
            # import errors
            from asyncpal import Error
            from asyncpal import BrokenPoolError
            from asyncpal import InitializerError
            from asyncpal import FinalizerError
            from asyncpal import InvalidStateError
            from asyncpal import CancelledError
        except ImportError:
            self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()
