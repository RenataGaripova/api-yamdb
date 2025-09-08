from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from api.filters import TitleFilter
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
)
from api.viewsets import (
    AuthenticatedCreateMixin,
    ListCreateDestroyViewSet,
    OwnerModeratorAdminEditMixin,
    PermissionsGrantMixin,
    ReadOnlyMixin,
)
from reviews.models import Category, Comment, Genre, Review, Title


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
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']


class ReviewViewSet(
    ReadOnlyMixin,
    AuthenticatedCreateMixin,
    OwnerModeratorAdminEditMixin,
    viewsets.ModelViewSet
):
    """ViewSet, реализующий CRUD к модели Review."""

    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(
    ReadOnlyMixin,
    AuthenticatedCreateMixin,
    OwnerModeratorAdminEditMixin,
    viewsets.ModelViewSet
):
    """ViewSet, реализующий CRUD к модели Comment."""

    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_review(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(
            Review,
            id=review_id,
            title_id=title_id
        )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        title = get_object_or_404(Title, id=title_id)
        review = get_object_or_404(Review, id=review_id, title=title)
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)
