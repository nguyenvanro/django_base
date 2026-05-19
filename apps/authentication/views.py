from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from apps.common.responses import APIResponse

from .schemas import (
    login_schema,
    logout_schema,
    me_schema,
    refresh_schema,
    verify_schema,
)


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    @login_schema
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return APIResponse.success(data=response.data, message="Login successful")


class RefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)

    @refresh_schema
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return APIResponse.success(data=response.data, message="Token refreshed")


class LogoutView(TokenBlacklistView):
    permission_classes = (AllowAny,)

    @logout_schema
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return APIResponse.success(message="Logged out successfully")


class VerifyView(TokenVerifyView):
    permission_classes = (AllowAny,)

    @verify_schema
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return APIResponse.success(message="Token is valid")


class MeView(APIView):
    permission_classes = (IsAuthenticated,)

    @me_schema
    def get(self, request):
        user = request.user
        return APIResponse.success(
            data={
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            message="Profile fetched successfully.",
        )
