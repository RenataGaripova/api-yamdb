from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError


class UsernameValidator(UnicodeUsernameValidator):
    """Кастомный валидатор имени пользователя с проверкой на 'me'."""

    def __call__(self, value):
        super().__call__(value)
        if value.lower() == 'me':
            raise ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
