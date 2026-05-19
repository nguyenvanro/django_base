from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler

from .responses import APIResponse


def custom_exception_handler(exc, context):
    """Wrap every DRF exception into the APIResponse envelope."""
    response = exception_handler(exc, context)

    if response is None:
        return None

    data = response.data

    if isinstance(exc, ValidationError):
        message = "Validation failed"
        errors = data
    elif isinstance(data, dict) and "detail" in data:
        message = str(data["detail"])
        errors = None
    elif isinstance(data, list) and data:
        message = str(data[0])
        errors = None
    else:
        message = "Error"
        errors = data

    return APIResponse(
        message=message,
        errors=errors,
        status_code=response.status_code,
    )
