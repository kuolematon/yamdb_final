from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOISES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    username = models.TextField(
        verbose_name='User',
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role', ]

    email = models.EmailField(
        verbose_name='Email',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    password = models.CharField(
        max_length=255,
        blank=False,
        null=True
    )
    bio = models.TextField(
        verbose_name='О себе',
        blank=True,
        null=True
    )
    role = models.CharField(
        verbose_name='Права',
        max_length=10,
        choices=ROLE_CHOISES,
        default=USER
    )
    first_name = models.TextField(
        verbose_name='Имя',
        max_length=150,
        null=True
    )
    last_name = models.TextField(
        verbose_name='Фамилия',
        max_length=150,
        null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        ordering = ['-id']

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.email
