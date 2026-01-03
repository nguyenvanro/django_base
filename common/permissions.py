from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed


class IsAuthenticatedCustom(IsAuthenticated):
    """
    Custom permission to check if the user is authenticated.
    """

    message = "You are not authenticated"
    
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            raise AuthenticationFailed(self.message)
        return True