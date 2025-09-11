from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.settings import AUTH_USER_MODEL
from reviews.constants import COMMENT_STR_LENGTH, REVIEW_STR_LENGTH
from reviews.validators import validate_year


class BaseNameModel(models.Model):
    """Абстрактная модель с именем."""
    name = models.CharField(max_length=256, verbose_name='Название')

    class Meta:
        abstract = True


class Category(BaseNameModel):
    """Модель категории."""

    slug = models.SlugField(unique=True, verbose_name='Слаг')

    def __str__(self):
        return f'Категория - {self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Genre(BaseNameModel):
    """Модель жанра."""

    slug = models.SlugField(unique=True, verbose_name='Слаг')

    def __str__(self):
        return f'Жанр - {self.name}'

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['id']


class Title(BaseNameModel):
    """Модель произведения."""

    year = models.SmallIntegerField(
        validators=[validate_year],
        verbose_name='Год выпуска',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True,
    )

    def __str__(self):
        return f'Произведение - {self.name}'

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
        ordering = ['year']


class Review(BaseNameModel):
    """Модель отзыва."""

    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='автор',
        help_text='Автор отзыва'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='произведение',
        help_text='Для какого произведения отзыв'
    )
    text = models.TextField(
        verbose_name='текст',
        help_text='Текст отзыва'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='дата создания',
        help_text='Дата и время создания комментария'
    )
    score = models.IntegerField(
        verbose_name='оценка',
        help_text='Оценка произведения',
        validators=[
            MinValueValidator(1, 'Оценка не может быть меньше 1'),
            MaxValueValidator(10, 'Оценка не может быть больше 10')
        ]
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review_per_author'
            )
        ]

    def __str__(self):
        return self.text[:REVIEW_STR_LENGTH]


class Comment(BaseNameModel):
    """Модель комментария."""

    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='автор',
        help_text='Автор комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='отзыв',
        help_text='Для какого отзыва комментарий'
    )
    text = models.TextField(
        verbose_name='текст',
        help_text='Текст комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата создания',
        help_text='Дата и время создания комментария'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)
        default_related_name = 'comments'

    def __str__(self):
        return self.text[:COMMENT_STR_LENGTH]
