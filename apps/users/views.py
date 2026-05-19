from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from apps.common.permissions import IsOwnerOrAdmin
from apps.common.responses import APIResponse

from .schemas import (
    change_password_schema,
    user_delete_schema,
    user_list_schema,
    user_register_schema,
    user_retrieve_schema,
    user_update_schema,
)
from .serializers import (
    PasswordChangeSerializer,
    UserCreateSerializer,
    UserSerializer,
    UserUpdateSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer

    _action_serializers = {
        "create": UserCreateSerializer,
        "update": UserUpdateSerializer,
        "partial_update": UserUpdateSerializer,
        "change_password": PasswordChangeSerializer,
    }

    _action_permissions = {
        "create": (AllowAny,),
        "list": (IsAuthenticated, IsAdminUser),
        "destroy": (IsAuthenticated, IsAdminUser),
    }

    def get_serializer_class(self):
        return self._action_serializers.get(self.action, self.serializer_class)

    def get_permissions(self):
        classes = self._action_permissions.get(
            self.action, (IsAuthenticated, IsOwnerOrAdmin)
        )
        return [c() for c in classes]

    @user_register_schema
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return APIResponse.created(
            data=UserSerializer(user).data, message="User registered"
        )

    @user_list_schema
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated = self.get_paginated_response(serializer.data)
            return APIResponse.success(
                data=paginated.data, message="Users fetched"
            )
        serializer = self.get_serializer(queryset, many=True)
        return APIResponse.success(data=serializer.data, message="Users fetched")

    @user_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return APIResponse.success(data=serializer.data, message="User fetched")

    @user_update_schema
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return APIResponse.success(
            data=UserSerializer(instance).data, message="User updated"
        )

    @user_update_schema
    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    @user_delete_schema
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return APIResponse.success(message="User deleted")

    @change_password_schema
    @action(detail=True, methods=["post"], url_path="change-password")
    def change_password(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not instance.check_password(serializer.validated_data["old_password"]):
            return APIResponse.error(
                message="Old password is incorrect",
                errors={"old_password": ["Old password is incorrect"]},
            )

        instance.set_password(serializer.validated_data["new_password"])
        instance.save(update_fields=["password"])
        return APIResponse.success(message="Password changed")
