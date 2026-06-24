from typing import Any

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(
    exc: Exception,
    context: dict[str, Any],
) -> Response | None:
    """Custom exception handler implementing LLD error envelope format.

    Args:
        exc: The exception that was raised.
        context: The context dictionary.

    Returns:
        Response with error envelope or None.
    """
    response = exception_handler(exc, context)

    if response is None:
        return response

    error_code: str
    error_message: str
    error_details: dict[str, Any] | None = None

    if isinstance(exc, ValidationError):
        error_code = "VALIDATION_ERROR"
        error_message = "Validation failed"
        error_details = response.data
    elif isinstance(exc, AuthenticationFailed):
        error_code = "AUTHENTICATION_ERROR"
        error_message = str(exc.detail) if exc.detail else "Authentication failed"
        if isinstance(exc.detail, list):
            error_message = exc.detail[0] if exc.detail else "Authentication failed"
    elif isinstance(exc, PermissionDenied):
        error_code = "PERMISSION_ERROR"
        error_message = str(exc.detail) if exc.detail else "Permission denied"
        if isinstance(exc.detail, list):
            error_message = exc.detail[0] if exc.detail else "Permission denied"
    elif isinstance(exc, NotFound):
        error_code = "NOT_FOUND_ERROR"
        error_message = str(exc.detail) if exc.detail else "Resource not found"
    else:
        error_code = "SERVER_ERROR"
        error_message = "An unexpected error occurred"

    response.data = {"error": {"code": error_code, "message": error_message}}

    if error_details is not None:
        response.data["error"]["details"] = error_details

    return response
