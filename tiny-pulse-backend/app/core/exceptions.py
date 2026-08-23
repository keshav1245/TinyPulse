"""Shared domain exceptions raised by the service layer."""


class AppError(Exception):
    """Base class for domain-level errors that carry their own HTTP status"""

    status_code: int = 500

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class NotFoundError(AppError):
    """Raised when a requested resource does not exist"""

    status_code = 404


class ConflictError(AppError):
    """Raised when an action conflicts with existing state, e.g. a duplicate"""

    status_code = 409
