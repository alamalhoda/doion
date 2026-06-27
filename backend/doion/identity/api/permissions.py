from rest_framework import permissions
from doion.users.models import User


class IsOwnerOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return request.user.profile.role in ["moderator", "admin"]


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role in ["moderator", "admin"]
