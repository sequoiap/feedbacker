"""Feedbacker exceptions."""


class FeedbackerException(Exception):
    """Base class for feedbacker exceptions."""


class RequiresLoginException(FeedbackerException):
    """Exception raised when a user is not logged in."""


class AutograderException(FeedbackerException):
    """Base class for exceptions during autograding."""

    def __init__(self, message: str, *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.message = message
