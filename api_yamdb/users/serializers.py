import random
import string

from rest_framework import serializers
from rest_framework.exceptions import NotFound

from django.conf import settings
from django.core.mail import send_mail

from .models import CustomUser


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации новых пользователей."""
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def validate_username(self, value):
        import re
        pattern = r'^[\w.@+-]+\Z'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                'Username может содержать только буквы, цифры и @/./+/-/_'
            )
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return value

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        user_by_email = CustomUser.objects.filter(email=email).first()
        user_by_username = CustomUser.objects.filter(username=username).first()

        if user_by_email and user_by_username:
            if user_by_email != user_by_username:
                raise serializers.ValidationError(
                    'Пользователь с таким email уже существует.'
                )

        if user_by_email and not user_by_username:
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )

        if user_by_username and not user_by_email:
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует.'
            )

        self.context['existing_user'] = user_by_email or user_by_username

        return data

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']

        user = self.context.get('existing_user')

        if user:
            user.email = email
            user.username = username
            user.is_active = False
        else:
            user = CustomUser.objects.create(
                username=username,
                email=email,
                is_active=False
            )

        user.confirmation_code = ''.join(
            random.choices(string.ascii_letters + string.digits, k=10)
        )
        user.save()

        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код: {user.confirmation_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return user


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT-токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        try:
            user = CustomUser.objects.get(username=username)
            if user.confirmation_code == confirmation_code:
                data['user'] = user
                return data
            raise serializers.ValidationError('Неверный код подтверждения.')
        except CustomUser.DoesNotExist:
            raise NotFound('Пользователь с таким username не найден.')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с пользователями."""
    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )

    def validate_username(self, value):
        import re
        pattern = r'^[\w.@+-]+\Z'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                'Username может содержать только буквы, цифры и @/./+/-/_'
            )
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return value


class UserMeSerializer(serializers.ModelSerializer):
    """Сериализатор для работы со своим профилем."""
    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)

    def validate_username(self, value):
        import re
        pattern = r'^[\w.@+-]+\Z'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                'Username может содержать только буквы, цифры и @/./+/-/_'
            )
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return value
