from rest_framework.permissions import BasePermission


class IsModeratorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "role", None) in ("moderator", "admin")
        )
