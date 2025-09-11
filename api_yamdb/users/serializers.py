from rest_framework import serializers

from django.contrib.auth.tokens import default_token_generator
from django.core.validators import EmailValidator
from django.shortcuts import get_object_or_404

from .constants import (
    MAX_LENGTH_CONFIRMATION_CODE,
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_USERNAME,
)
from .models import YamdbUser
from .validators import UsernameValidator


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации новых пользователей."""
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME,
        validators=[UsernameValidator()]
    )
    email = serializers.EmailField(
        max_length=MAX_LENGTH_EMAIL,
        validators=[EmailValidator()]
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

        self.context['existing_user'] = user_by_email or user_by_username

        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT-токена."""
    username = serializers.CharField(validators=[UsernameValidator()])
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
