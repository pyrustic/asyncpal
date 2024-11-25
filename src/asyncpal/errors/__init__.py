"""Errors raised by the library"""


class Error(Exception):
    pass


class RemoteTraceback(Error):
    """An instance of this class is available on the
     __context__ attribute of the last remote exception in an
     exception chain that occurred in a ProcessPool.
     """
    def __init__(self, traceback_lines):
        self._traceback_lines = traceback_lines

    @property
    def traceback_lines(self):
        return self._traceback_lines

    def __str__(self):
        tbs = "".join(self._traceback_lines)
        return '\n"""\n{}"""'.format(tbs)


class InvalidStateError(Error):
    pass


class CancelledError(Error):
    pass


class BrokenPoolError(Error):
    pass


class InitializerError(BrokenPoolError):
    pass


class FinalizerError(BrokenPoolError):
    pass
