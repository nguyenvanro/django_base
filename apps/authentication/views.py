from rest_framework.views import APIView
from apps.authentication.serializers import LoginSerializer
from common.responses import BaseResponseMixin
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

class TokenSerializer(serializers.Serializer):
    """Serializer for token"""

    access = serializers.CharField()
    refresh = serializers.CharField()

    @staticmethod
    def get_token_for_user(user):
        """Get token for user"""
        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
        

class LoginView(APIView, BaseResponseMixin):
    """View for login"""

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token_data = TokenSerializer.get_token_for_user(user)

        return self.success_res(data=token_data, message="Login successfully")