"""
Exceptions for the Incus Python SDK.
"""

from typing import Dict, Any, Optional


class IncusError(Exception):
    """Base exception for all Incus errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a new IncusError.

        Args:
            message: Error message.
            status_code: HTTP status code.
            response: API response.
        """
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(message)


class IncusAPIError(IncusError):
    """Exception raised when an API request fails."""

    def __init__(
        self, message: str, status_code: int, response: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a new IncusAPIError.

        Args:
            message: Error message.
            status_code: HTTP status code.
            response: API response.
        """
        super().__init__(message, status_code, response)


class IncusConnectionError(IncusError):
    """Exception raised when a connection to the Incus API fails."""

    def __init__(self, message: str, cause: Optional[Exception] = None):
        """
        Initialize a new IncusConnectionError.

        Args:
            message: Error message.
            cause: Original exception.
        """
        self.cause = cause
        super().__init__(message)


class IncusOperationError(IncusError):
    """Exception raised when an operation fails."""

    def __init__(
        self, message: str, operation_id: str, response: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a new IncusOperationError.

        Args:
            message: Error message.
            operation_id: ID of the failed operation.
            response: Operation response.
        """
        self.operation_id = operation_id
        super().__init__(message, response=response)


class IncusNotFoundError(IncusAPIError):
    """Exception raised when a resource is not found."""

    def __init__(self, message: str, response: Optional[Dict[str, Any]] = None):
        """
        Initialize a new IncusNotFoundError.

        Args:
            message: Error message.
            response: API response.
        """
        super().__init__(message, 404, response)


class IncusAuthenticationError(IncusAPIError):
    """Exception raised when authentication fails."""

    def __init__(
        self,
        message: str,
        status_code: int = 401,
        response: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a new IncusAuthenticationError.

        Args:
            message: Error message.
            status_code: HTTP status code.
            response: API response.
        """
        super().__init__(message, status_code, response)


class IncusPermissionError(IncusAPIError):
    """Exception raised when permission is denied."""

    def __init__(self, message: str, response: Optional[Dict[str, Any]] = None):
        """
        Initialize a new IncusPermissionError.

        Args:
            message: Error message.
            response: API response.
        """
        super().__init__(message, 403, response)
