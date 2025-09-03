from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from artworks.models import Category, Genre, Title
from .viewsets import ListCreateDestroyViewSet, PermissionsGrantMixin
from .serializers import CategorySerializer, TitleSerializer, GenreSerializer


class CategoryViewSet(PermissionsGrantMixin, ListCreateDestroyViewSet):
    """ViewSet, реализующий GET, POST и DELETE запросы к модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(PermissionsGrantMixin, ListCreateDestroyViewSet):
    """ViewSet, реализующий GET, POST и DELETE запросы к модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(PermissionsGrantMixin, viewsets.ModelViewSet):
    """ViewSet, реализующий CRUD к модели Title."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['category', 'genre', 'name', 'year']
