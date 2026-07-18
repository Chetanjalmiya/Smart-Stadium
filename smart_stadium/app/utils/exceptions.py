"""Custom application exceptions."""


class AppException(Exception):
    """Base application exception carrying an HTTP status code."""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(AppException):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str, identifier: object):
        super().__init__(
            message=f"{resource} with id '{identifier}' was not found.",
            status_code=404,
        )


class ValidationException(AppException):
    """Raised when input data fails business validation rules."""

    def __init__(self, message: str):
        super().__init__(message=message, status_code=422)


class ConflictException(AppException):
    """Raised when an operation conflicts with the current resource state."""

    def __init__(self, message: str):
        super().__init__(message=message, status_code=409)


class UnauthorizedException(AppException):
    """Raised when authentication/authorization fails."""

    def __init__(self, message: str = "Unauthorized access."):
        super().__init__(message=message, status_code=401)
