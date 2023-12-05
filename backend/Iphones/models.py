from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from users.models import User


class IphoneDiagonal(models.Model):
    diagonal = models.CharField(
        verbose_name="Диагональ",
        max_length=30,
        unique=True,
    )
    # diagonal = models.CharField(
    #     verbose_name="Диагональ",
    #     max_length=100,
    # )
    # type_of_screen = models.CharField(
    #     verbose_name="Тип",
    #     max_length=100,
    # )
    # resolution = models.CharField(
    #     verbose_name="Разрешение",
    #     max_length=50,
    # )
    # brightness = models.CharField(
    #     verbose_name="Яркость",
    #     max_length=50,
    # )
    #
    # CONTRAST_CHOICES = [
    #     ("сontrast_1400", "1400:1"),
    #     ("сontrast_2000000", "2000000:1"),
    # ]
    # pixel_procity = models.CharField(
    #     verbose_name="пикс/дюйм",
    #     max_length=50,
    # )
    #
    # contrast = models.CharField(verbose_name="Контрастность", max_length=50, choices=CONTRAST_CHOICES)

    def __str__(self):
        return self.diagonal


class IphoneTypeOfScreen(models.Model):
    screen = models.CharField(
        verbose_name="Тип экрана",
        max_length=30,
        unique=True,
    )

    def __str__(self):
        return self.screen


class IphoneCountCamera(models.Model):
    camera = models.CharField(
        verbose_name="Количество камер",
        max_length=15,
        unique=True,
    )
    def __str__(self):
        return self.camera


class IphoneProcessor(models.Model):
    processor = models.CharField(
        verbose_name="Процессор",
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.processor


class IphoneColor(models.Model):
    color = models.CharField(
        verbose_name="Цвет",
        max_length=30,
        unique=True
    )
    slug = models.SlugField(
        verbose_name="Слаг",
        unique=True,
        max_length=200
    )

    def __str__(self):
        return self.color


class IphoneRom(models.Model):
    # ROM_CHOICES = [
    #     ("64", "64GB"),
    #     ("128", "128GB"),
    #     ("256", "256GB"),
    #     ("512", "512GB"),
    #     ("1024", "1024GB")
    # ]
    rom = models.CharField(
        max_length=10,
        verbose_name="Объем памяти",
    )

    def __str__(self):
        return f"{self.rom}GB"


class IphoneMobileConnection(models.Model):
    mobile_connection = models.CharField(
        verbose_name="Связь",
        max_length=50,
    )

    def __str__(self):
        return self.mobile_connection


class IphoneModel(models.Model):
    model = models.CharField(
        verbose_name="Модель iPhone",
        max_length=100,
    )

    def __str__(self):
        return self.model


class Iphone(models.Model):
    model = models.ForeignKey(
        IphoneModel,
        verbose_name="Модель iPhone",
        max_length=100,
        on_delete=models.CASCADE,
    )
    image = models.ImageField()
    text = models.TextField(verbose_name="Текстовое описание")
    color = models.ForeignKey(
        IphoneColor,
        verbose_name="Цвет",
        # related_name="iPhones",
        on_delete=models.CASCADE
    )
    rom = models.ForeignKey(
        IphoneRom,
        verbose_name="Память",
        max_length=50,
        on_delete=models.CASCADE
    )
    CONNECTION_CHOICES = [
        ("SIM_ESIM", "SIM/ESIM"),
        ("DUAL_SIM", "DUAL_SIM"),
        ("ESIM", "ESIM"),
    ]
    mobile_connection = models.ForeignKey(
        IphoneMobileConnection,
        verbose_name="Связь",
        max_length=50,
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(
        verbose_name="Цена iPhone",
        max_digits=15,
        decimal_places=2
    )
    processor = models.ForeignKey(
        IphoneProcessor,
        verbose_name="Процессор iPhone",
        max_length=50,
        on_delete=models.CASCADE
    )
    camera = models.ForeignKey(
        IphoneCountCamera,
        verbose_name="Количство камер",
        max_length=15,
        on_delete=models.CASCADE,
    )
    diagonal = models.ForeignKey(
        IphoneDiagonal,
        verbose_name="Диагональ",
        max_length=50,
        on_delete=models.CASCADE
    )
    type_of_screen = models.ForeignKey(
        IphoneTypeOfScreen,
        verbose_name="Тип экрана",
        max_length=50,
        on_delete=models.CASCADE,
    )
    resolution = models.CharField(
        verbose_name="Разрешение",
        max_length=50,
    )
    brightness = models.CharField(
        verbose_name="Яркость",
        max_length=50,
    )

    CONTRAST_CHOICES = [
        ("сontrast_1400", "1400:1"),
        ("сontrast_2000000", "2000000:1"),
    ]
    contrast = models.CharField(
        verbose_name="Контрастность",
        max_length=50,
        choices=CONTRAST_CHOICES
    )
    pixel_procity = models.CharField(
        verbose_name="пикс/дюйм",
        max_length=50,
    )

    class Meta:
        verbose_name = 'iPhone'
        verbose_name_plural = 'iPhones'

    def __str__(self):
        return f"{self.model} {self.rom}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Добавил в избранное",
        related_name="favorite_user",
        on_delete=models.CASCADE,
    )
    price_at_purchase = models.DecimalField(
        verbose_name="Цена при покупке",
        max_digits=15,
        decimal_places=2,
    )
    iphone = models.ForeignKey(
        Iphone,
        verbose_name="iPhone",
        related_name="favorite",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Избранный iPhone"
        verbose_name_plural = "Избранные iPhones"
        unique_together = (
            "user",
            "iphone"
        )

    def __str__(self):
        return f"{self.user} added {self.iphone}"

    def save(self, *args, **kwargs):
        # Присваиваем цену при покупке перед сохранением объекта
        self.price_at_purchase = self.iphone.price
        super().save(*args, **kwargs)


class ShoppingCart(models.Model):
    iphone = models.ForeignKey(
        Iphone,
        verbose_name="iPhone в корзине",
        related_name="shopping_cart",
        on_delete=models.CASCADE,
    )
    price_at_purchase = models.DecimalField(
        verbose_name="Цена при покупке",
        max_digits=15,
        decimal_places=2,
    )
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        related_name="shopping_cart",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Список покупки"
        verbose_name_plural = "Список покупок"

        # Делаем эти значения в бд уникальными
        unique_together = (
            "user",
            "iphone"
        )

    def __str__(self):
        return f"{self.user} added {self.iphone}"

    def save(self, *args, **kwargs):
        # Присваиваем цену при покупке перед сохранением объекта
        self.price_at_purchase = self.iphone.price
        super().save(*args, **kwargs)

