from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers

from apps.common.openapi import envelope

USER_TAG = "Users"

_user_field = inline_serializer(
    name="UserData",
    fields={
        "id": serializers.IntegerField(),
        "username": serializers.CharField(),
        "email": serializers.EmailField(),
        "first_name": serializers.CharField(allow_blank=True),
        "last_name": serializers.CharField(allow_blank=True),
        "is_active": serializers.BooleanField(),
        "date_joined": serializers.DateTimeField(),
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


user_register_schema = extend_schema(
    tags=[USER_TAG],
    summary="Register",
    description="Create a new user account. Public endpoint.",
    responses={
        201: OpenApiResponse(
            response=envelope("UserRegisterSuccess", data_field=_user_field),
            examples=[_example("Success", 201, "User registered")],
        ),
        400: OpenApiResponse(
            response=envelope("UserRegisterError"),
            examples=[_example("Validation failed", 400, "Validation failed")],
        ),
    },
)


user_list_schema = extend_schema(
    tags=[USER_TAG],
    summary="List users",
    description="List all users (paginated). Admin only.",
    responses={200: OpenApiResponse(response=envelope("UserListSuccess"))},
)


user_retrieve_schema = extend_schema(
    tags=[USER_TAG],
    summary="Retrieve user",
    description="Fetch a single user. Owner or admin only.",
    responses={
        200: OpenApiResponse(
            response=envelope("UserRetrieveSuccess", data_field=_user_field)
        ),
    },
)


user_update_schema = extend_schema(
    tags=[USER_TAG],
    summary="Update user",
    description="Update profile fields (email, first_name, last_name). Owner or admin only.",
    responses={
        200: OpenApiResponse(
            response=envelope("UserUpdateSuccess", data_field=_user_field)
        ),
    },
)


user_delete_schema = extend_schema(
    tags=[USER_TAG],
    summary="Delete user",
    description="Delete a user account. Admin only.",
    responses={
        200: OpenApiResponse(
            response=envelope("UserDeleteSuccess"),
            examples=[_example("Success", 200, "User deleted")],
        ),
    },
)


change_password_schema = extend_schema(
    tags=[USER_TAG],
    summary="Change password",
    description="Change a user's password. Requires the current password. Owner or admin only.",
    responses={
        200: OpenApiResponse(
            response=envelope("ChangePasswordSuccess"),
            examples=[_example("Success", 200, "Password changed")],
        ),
        400: OpenApiResponse(
            response=envelope("ChangePasswordError"),
            examples=[_example("Wrong old password", 400, "Old password is incorrect")],
        ),
    },
)
