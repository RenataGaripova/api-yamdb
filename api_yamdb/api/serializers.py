from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.db.models import Avg

from reviews.models import Category, Genre, Title, Review, Comment


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


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

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
        extra_kwargs = {
            'description': {'required': False}
        }

    def get_rating(self, obj):
        avg_rating = obj.reviews.aggregate(Avg('score'))['score__avg']
        return avg_rating if avg_rating is not None else None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["category"] = (
            CategorySerializer(instance.category).data
            if instance.category else None
        )
        data["genre"] = GenreSerializer(instance.genre.all(), many=True).data
        return data


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

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title = self.context['view'].get_title()
            user = self.context['request'].user
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
