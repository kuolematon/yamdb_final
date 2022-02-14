from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from titles.models import Title
from users.models import User


class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[
            MaxValueValidator(10, message='Максимальный рейтинг 10'),
            MinValueValidator(1, message='Минимальный рейтинг 1')
        ]
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=True,
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                name='unique_review',
                fields=['author', 'title'],
            ),
        ]

    def __str__(self):
        return (f'{self.author.get_full_name()} review '
                f'to title {self.title.name}')


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='comments',
        blank=True,
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        blank=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return (f'{self.author.get_full_name()} comment '
                f'to title {self.title.name}')
