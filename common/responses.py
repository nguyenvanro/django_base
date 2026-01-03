from rest_framework import status
from rest_framework.response import Response


class BaseResponseMixin:
    """
    Base mixin for standardized API responses.
    """

    def success_res(
        self,
        message: str = "Success",
        data=None,
        status_code: int = status.HTTP_200_OK,
        paginator=None,
        totals: dict | None = None,
        extra: dict | None = None,
    ) -> Response:
        if paginator is not None and hasattr(paginator, "page"):
            response_data = {
                "count": paginator.page.paginator.count,
                "total_pages": paginator.page.paginator.num_pages,
                "current_page": paginator.page.number,
                "page_size": paginator.get_page_size(paginator.request),
                "results": data,
            }

            if totals:
                response_data["totals"] = totals
        else:
            response_data = data

        payload = {
            "status": status_code,
            "message": message,
            "data": response_data,
        }

        if extra:
            payload.update(extra)

        return Response(payload, status=status_code)

    def error_res(
        self,
        message: str = "Error",
        errors: dict | list | str | None = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        code: str | None = None,
        extra: dict | None = None,
    ) -> Response:
        payload = {
            "status": status_code,
            "message": message,
        }

        if code:
            payload["code"] = code

        if errors:
            payload["errors"] = errors

        if extra:
            payload.update(extra)

        return Response(payload, status=status_code)
