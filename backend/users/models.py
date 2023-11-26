from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = (
        'id',
        'password',
        'first_name',
        'last_name',
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
        unique=True, blank=False
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=30,
        blank=False
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=30,
        blank=False
    )