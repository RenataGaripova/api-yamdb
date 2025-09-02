from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin
)
from rest_framework import permissions

from rest_framework.viewsets import GenericViewSet


class ListCreateDestroyViewSet(
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin
):
    """Миксин для получения списка объектов, создания и удаления объекта."""

    pass


class PermissionsGrantMixin:
    """Миксин для определения прав пользователя."""

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
