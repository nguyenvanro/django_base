from rest_framework import status
from rest_framework.response import Response


class APIResponse(Response):
    """Standardized envelope: {status_code, message, data, errors}."""

    def __init__(
        self,
        data=None,
        message="",
        errors=None,
        status_code=status.HTTP_200_OK,
        **kwargs,
    ):
        payload = {
            "status_code": status_code,
            "message": message,
            "data": data,
            "errors": errors,
        }
        super().__init__(data=payload, status=status_code, **kwargs)

    @classmethod
    def success(cls, data=None, message="Success", status_code=status.HTTP_200_OK):
        return cls(data=data, message=message, status_code=status_code)

    @classmethod
    def created(cls, data=None, message="Created"):
        return cls(data=data, message=message, status_code=status.HTTP_201_CREATED)

    @classmethod
    def error(
        cls,
        message="Error",
        errors=None,
        status_code=status.HTTP_400_BAD_REQUEST,
    ):
        return cls(message=message, errors=errors, status_code=status_code)
