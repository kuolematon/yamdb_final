from django.db import models

from .validators import year_validator


class Category(models.Model):
    """Модель Категорий"""
    name = models.CharField(verbose_name='Название', max_length=256)
    slug = models.SlugField(
        verbose_name='Слаг', max_length=50, unique=True, db_index=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(verbose_name='Название', max_length=256)
    slug = models.SlugField(
        verbose_name='Слаг', max_length=50, unique=True, db_index=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(
        verbose_name='Название', max_length=256, db_index=True
    )
    year = models.IntegerField(
        verbose_name='Год выпуска', validators=(year_validator,)
    )
    description = models.CharField(verbose_name='Описание', max_length=300)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', null=True, blank=True, verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return (f'Название: {self.name}, описание: {self.description[:20]},'
                f'Год выпуска: {self.year}')
