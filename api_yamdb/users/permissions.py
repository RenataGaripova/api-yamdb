from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Permission, проверяющий, что пользователь - администратор."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsModerator(permissions.BasePermission):
    """Permission, проверяющий, что пользователь - модератор."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Permission, разрешающий запись только владельцу."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsOwnerOrModeratorOrAdmin(permissions.BasePermission):
    """
    Permission, разрешающий запись только владельцу, модераторам и
    администраторам.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        return (obj.author == request.user
                or request.user.is_moderator or request.user.is_admin)
