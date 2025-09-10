from django.db.models import Avg, IntegerField, ExpressionWrapper
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from api.filters import TitleFilter
from reviews.models import Category, Genre, Review, Title
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
    queryset = Title.objects.all().annotate(
        rating=ExpressionWrapper(
            Avg('reviews__score'),
            output_field=IntegerField()
        )
    )
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
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


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
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=get_object_or_404(Title, id=self.kwargs.get('title_id'))
        )
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
