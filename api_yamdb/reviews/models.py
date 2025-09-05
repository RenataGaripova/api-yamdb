from django.db import models

from api_yamdb.settings import AUTH_USER_MODEL
from reviews.constants import COMMENT_STR_LENGTH, REVIEW_STR_LENGTH


class BaseModel(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:

        abstract = True


class Category(BaseModel):
    """Модель категории."""

    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(BaseModel):
    """Модель жанра."""

    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(BaseModel):
    """Модель произведения."""

    year = models.IntegerField(verbose_name='Год выпуска')
    rating = models.IntegerField(default=1, verbose_name='Рейтинг')
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True,
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'


class Review(BaseModel):
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
        blank=False,
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
        default=1,
        choices=((i, i) for i in range(1, 11)),
        verbose_name='оценка',
        help_text='Оценка произведения'
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        default_related_name = 'reviews'

    def __str__(self):
        return self.text[:REVIEW_STR_LENGTH]


class Comment(BaseModel):
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
        blank=False,
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
        ordering = ['-pub_date']
        default_related_name = 'comments'

    def __str__(self):
        return self.text[:COMMENT_STR_LENGTH]
