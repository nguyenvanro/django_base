from rest_framework.views import APIView
from common.responses import BaseResponseMixin
from rest_framework.permissions import IsAuthenticated
from apps.users.serializers import UserSerializer


class UserView(APIView, BaseResponseMixin):
    """View for user"""

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return self.success_res(data=serializer.data)