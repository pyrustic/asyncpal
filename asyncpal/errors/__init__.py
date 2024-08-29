"""Errors raised by the library"""


class Error(Exception):
    pass


class RemoteError(Error):
    """An object of this class is available on the
     __context__ attribute of any remote exception
     in a ProcessPool. This class has zero link with ThreadPool.
     """
    def __init__(self, traceback_str, exc_chain):
        self._traceback_str = traceback_str
        self._exc_chain = tuple(exc_chain) if exc_chain else tuple()
    
    @property
    def exc_chain(self):
        return self._exc_chain
    
    def __str__(self):
        return self._traceback_str


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
