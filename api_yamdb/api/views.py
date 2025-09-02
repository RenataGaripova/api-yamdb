from rest_framework import viewsets, permissions
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from artworks.models import Category, Genre, Title
from .viewsets import ListCreateDestroyViewSet, PermissionsGrantMixin
from .serializers import CategorySerializer, TitleSerializer, GenreSerializer


class CategoryViewSet(ListCreateDestroyViewSet, PermissionsGrantMixin):
    """ViewSet, реализующий GET, POST и DELETE запросы к модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class GenreViewSet(ListCreateDestroyViewSet, PermissionsGrantMixin):
    """ViewSet, реализующий GET, POST и DELETE запросы к модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet, PermissionsGrantMixin):
    """ViewSet, реализующий CRUD к модели Title."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['category', 'genre', 'name', 'year']
