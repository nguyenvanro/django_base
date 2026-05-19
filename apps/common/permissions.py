from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """Allow access when the requesting user owns the object or is staff."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_staff:
            return True
        return obj == user
