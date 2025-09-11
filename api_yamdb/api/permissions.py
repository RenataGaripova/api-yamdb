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
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Permission, разрешающий запись и изменение только админу."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )
