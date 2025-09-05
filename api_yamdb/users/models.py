from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""

    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
    )

    email = models.EmailField(
        'email address',
        unique=True,
        max_length=254,
    )
    bio = models.TextField(
        'биография',
        blank=True,
        null=True,
    )
    role = models.CharField(
        'роль',
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=100,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR
