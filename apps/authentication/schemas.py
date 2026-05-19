from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers

from apps.common.openapi import envelope

AUTH_TAG = "Authentication"

_tokens_field = inline_serializer(
    name="JWTTokens",
    fields={
        "access": serializers.CharField(),
        "refresh": serializers.CharField(),
    },
)

_me_field = inline_serializer(
    name="MeData",
    fields={
        "id": serializers.IntegerField(),
        "username": serializers.CharField(),
        "email": serializers.EmailField(),
    },
)


def _example(name, status_code, message, data=None):
    return OpenApiExample(
        name,
        value={
            "status_code": status_code,
            "message": message,
            "data": data,
            "errors": None,
        },
    )


login_schema = extend_schema(
    tags=[AUTH_TAG],
    summary="Login",
    description="Authenticate by username + password and obtain JWT access & refresh tokens.",
    responses={
        200: OpenApiResponse(
            response=envelope("LoginSuccess", data_field=_tokens_field),
            examples=[
                _example(
                    "Success",
                    200,
                    "Login successful",
                    {"access": "eyJhbGciOi...", "refresh": "eyJhbGciOi..."},
                )
            ],
        ),
        401: OpenApiResponse(
            response=envelope("LoginError"),
            examples=[
                _example(
                    "Invalid credentials",
                    401,
                    "No active account found with the given credentials",
                )
            ],
        ),
    },
)


refresh_schema = extend_schema(
    tags=[AUTH_TAG],
    summary="Refresh access token",
    description="Exchange a valid refresh token for a new access (and rotated refresh) token.",
    responses={
        200: OpenApiResponse(
            response=envelope("RefreshSuccess", data_field=_tokens_field),
            examples=[
                _example(
                    "Success",
                    200,
                    "Token refreshed",
                    {"access": "eyJhbGciOi...", "refresh": "eyJhbGciOi..."},
                )
            ],
        ),
        401: OpenApiResponse(
            response=envelope("RefreshError"),
            examples=[
                _example(
                    "Invalid or blacklisted refresh token",
                    401,
                    "Token is invalid or expired",
                )
            ],
        ),
    },
)


logout_schema = extend_schema(
    tags=[AUTH_TAG],
    summary="Logout",
    description="Blacklist the supplied refresh token so it can no longer be used.",
    responses={
        200: OpenApiResponse(
            response=envelope("LogoutSuccess"),
            examples=[_example("Success", 200, "Logged out successfully")],
        ),
    },
)


verify_schema = extend_schema(
    tags=[AUTH_TAG],
    summary="Verify token",
    description="Verify whether the supplied access or refresh token is still valid.",
    responses={
        200: OpenApiResponse(
            response=envelope("VerifySuccess"),
            examples=[_example("Success", 200, "Token is valid")],
        ),
        401: OpenApiResponse(
            response=envelope("VerifyError"),
            examples=[_example("Invalid token", 401, "Token is invalid or expired")],
        ),
    },
)


me_schema = extend_schema(
    tags=[AUTH_TAG],
    summary="Current user profile",
    description="Return information about the authenticated user.",
    responses={
        200: OpenApiResponse(
            response=envelope("MeSuccess", data_field=_me_field),
        ),
    },
)
