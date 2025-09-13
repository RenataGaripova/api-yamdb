from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title
from users.constants import (
    MAX_LENGTH_CONFIRMATION_CODE,
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_USERNAME,
)
from users.models import YamdbUser
from users.validators import UsernameValidator


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

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
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
    rating = serializers.IntegerField(default=None, read_only=True)

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


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для валидации данных."""
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME,
        validators=[UsernameValidator()]
    )
    email = serializers.EmailField(
        max_length=MAX_LENGTH_EMAIL,
    )

    class Meta:
        model = YamdbUser
        fields = ('email', 'username')

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        user_by_email = YamdbUser.objects.filter(email=email).first()
        user_by_username = YamdbUser.objects.filter(username=username).first()

        error_msg = {}

        if user_by_email != user_by_username:

            if user_by_email is not None:
                error_msg['email'] = [
                    'Пользователь с таким email уже существует.'
                ]

            if user_by_username is not None:
                error_msg['username'] = [
                    'Пользователь с таким username уже существует.'
                ]

        if error_msg:
            raise serializers.ValidationError(error_msg)

        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT-токена."""
    username = serializers.CharField(
        validators=[UsernameValidator()],
        max_length=MAX_LENGTH_USERNAME
    )
    confirmation_code = serializers.CharField(
        max_length=MAX_LENGTH_CONFIRMATION_CODE
    )

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        user = get_object_or_404(YamdbUser, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError('Неверный код подтверждения.')

        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с пользователями."""
    class Meta:
        model = YamdbUser
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class UserMeSerializer(serializers.ModelSerializer):
    """Сериализатор для работы со своим профилем."""
    class Meta:
        model = YamdbUser
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)
