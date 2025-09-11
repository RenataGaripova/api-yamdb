from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Permission, проверяющий, что пользователь - администратор."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """Permission, разрешающий запись и изменение только админу."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )


class IsOwnerModeratorAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает полный доступ владельцу, модератору и админу.
    Остальным — только чтение.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
