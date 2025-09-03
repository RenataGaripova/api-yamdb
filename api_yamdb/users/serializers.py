from rest_framework import serializers, status
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )

        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует.'
            )

        return data

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return value

    def create(self, validated_data):
        import random
        import string

        email = validated_data['email']
        username = validated_data['username']

        user, created = CustomUser.objects.get_or_create(
            email=email,
            username=username,
            defaults={'confirmation_code': ''.join(random.choices(
                string.ascii_letters + string.digits, k=10
            ))}
        )

        if not created:
            user.confirmation_code = ''.join(random.choices(
                string.ascii_letters + string.digits, k=10
            ))
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
            raise serializers.ValidationError(
                {'detail': 'Пользователь с таким username не найден.'},
                code=status.HTTP_404_NOT_FOUND
            )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio'
        )
        read_only_fields = ('role',)
