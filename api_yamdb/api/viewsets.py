from rest_framework import filters, permissions
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import OR
from rest_framework.viewsets import GenericViewSet

from .permissions import IsAdmin, IsModerator, IsOwnerOrReadOnly


class ListCreateDestroyViewSet(
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin
):
    """Миксин для получения списка объектов, создания и удаления объекта."""

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class PermissionsGrantMixin:
    """Миксин для определения прав пользователя."""

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]


class ReadOnlyMixin:
    """Только чтение для всех"""

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return super().get_permissions()


class AuthenticatedCreateMixin:
    """Аутентифицированные пользователи могут создавать"""

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return super().get_permissions()


class OwnerModeratorAdminEditMixin:
    """Владельцы, модераторы и админы могут редактировать/удалять"""

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [
                permissions.IsAuthenticated(),
                OR(OR(IsOwnerOrReadOnly(), IsModerator()), IsAdmin())
            ]
        return super().get_permissions()
