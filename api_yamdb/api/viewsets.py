from rest_framework import filters
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet

from api.permissions import IsAdminOrReadOnly


class CategoryGenreViewSet(
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
    permission_classes = (IsAdminOrReadOnly,)
