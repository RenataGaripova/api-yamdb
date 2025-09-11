from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models

from .constants import (
    MAX_LENGTH_BIO,
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_ROLE,
    MAX_LENGTH_USERNAME,
)
from .validators import UsernameValidator


class YamdbUser(AbstractUser):
    """Кастомная модель пользователя."""

    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    username = models.CharField(
        'username',
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
        validators=[UsernameValidator()],
    )

    email = models.EmailField(
        'email address',
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
        validators=[EmailValidator()],
    )
    bio = models.TextField(
        'биография',
        max_length=MAX_LENGTH_BIO,
        blank=True,
        null=True,
    )
    role = models.CharField(
        'роль',
        max_length=MAX_LENGTH_ROLE,
        choices=Role.choices,
        default=Role.USER,
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
