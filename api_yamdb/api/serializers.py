from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.db.models import Avg

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи и обноваления произведений."""
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(), 
        many=True,
        allow_empty=False,
    )
    rating = serializers.IntegerField(default=None)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'category',
            'genre'
        )

    def to_representation(self, instance):
        return TitleReadSerializer(instance).data


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения произведений."""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(default=None)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'category',
            'genre'
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        )

    def validate_score(self, value):
        """Валидация оценки только если она передана."""
        if value is not None and not 1 <= value <= 10:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10')
        return value

    def validate(self, data):
        """Валидация только для создания отзыва."""
        request = self.context['request']

        if request.method == 'POST':
            title = self.context['view'].get_title()
            user = request.user
            if Review.objects.filter(author=user, title=title).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли отзыв на это произведение'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date'
        )
