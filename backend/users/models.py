from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = (
        'id',
        'password',
        'first_name',
        'last_name',
        'username',
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
    username = models.CharField(
        verbose_name="Имя пользователя",
        max_length=30,
        blank=False
    )

    def save(self, *args, **kwargs):
        # ваша логика сохранения, если нужна
        if "password" in self.__dict__ and self.password:
            # если есть пароль, хэшируем его перед сохранением
            self.set_password(self.password)
        super().save(*args, **kwargs)
