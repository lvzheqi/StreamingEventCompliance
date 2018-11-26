class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class EventError(Error):
    """Exception raised for errors in the request.

    Attributes:
        event -- an event Object
    """

    def __init__(self, event):
        self.event = event


class NoUserError(Error):
    pass
