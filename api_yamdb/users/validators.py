from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError

from .constants import FORBIDDEN_USERNAMES


class UsernameValidator(UnicodeUsernameValidator):
    """Кастомный валидатор имени пользователя с проверкой на 'me'."""

    def __call__(self, value):
        super().__call__(value)
        if value.lower() in FORBIDDEN_USERNAMES:
            raise ValidationError(
                (f'Использовать имя "{value}" в качестве username запрещено.')
            )
