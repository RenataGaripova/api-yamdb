from django.db import models


class BaseModel(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:

        abstract = True


class Category(BaseModel):
    """Модель категории."""

    slug = models.SlugField(verbose_name='Слаг')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(BaseModel):
    """Модель жанра."""

    slug = models.SlugField(verbose_name='Слаг')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(BaseModel):
    """Модель произведения."""

    year = models.IntegerField(verbose_name='Год выпуска')
    rating = models.IntegerField(default=1, verbose_name='Рейтинг')
    description = models.TextField(verbose_name='Описание')
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        verbose_name='Жанр',
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True,
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
