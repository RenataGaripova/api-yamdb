from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    """Проверка года произведения."""

    if value > datetime.now().year:
        raise ValidationError(
            "Год выпуска не может превышать текущий."
        )
