from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from users.models import User


class ScreenIphone(models.Model):
    model = models.CharField(
        verbose_name="Экран для iPhone",
        max_length=50
        # on_delete=models.CASCADE
    )
    diagonal = models.CharField(
        verbose_name="Диагональ",
        max_length=100,
    )
    type_of_screen = models.CharField(
        verbose_name="Тип",
        max_length=100,
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
    pixel_procity = models.CharField(
        verbose_name="пикс/дюйм",
        max_length=50,
    )

    contrast = models.CharField(verbose_name="Контрастность", max_length=50, choices=CONTRAST_CHOICES)

    def __str__(self):
        return f"{self.model} iPhone"


class ProcessorIphone(models.Model):
    processor = models.CharField(
        verbose_name="Процессор",
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.processor


class Color(models.Model):
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
    ROM_CHOICES = [
        ("64", "64GB"),
        ("128", "128GB"),
        ("256", "256GB"),
        ("512", "512GB"),
        ("1024", "1024GB")
    ]
    model = models.CharField(verbose_name="Модель айфона", max_length=50,)
    rom = models.CharField(max_length=10, verbose_name="Объем памяти", choices=ROM_CHOICES)
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return f"iPhone {self.model} {self.rom}GB"


class Iphone(models.Model):
    model = models.CharField(
        verbose_name="Модель iPhone",
        max_length=256,
    )
    image = models.ImageField()
    text = models.TextField(verbose_name="Текстовое описание")
    color = models.ForeignKey(
        Color,
        verbose_name="Цвет",
        # related_name="iPhones",
        on_delete=models.CASCADE
    )
    rom = models.ForeignKey(
        IphoneRom,
        verbose_name="Память",
        related_name="iPhones",
        on_delete=models.CASCADE,
    )
    CONNECTION_CHOICES = [
        ("SIM_ESIM", "SIM/ESIM"),
        ("DUAL_SIM", "DUAL_SIM"),
        ("ESIM", "ESIM"),
    ]
    mobile_connection = models.CharField(
        verbose_name="Связь",
        max_length=50,
        choices=CONNECTION_CHOICES,
    )
    price = models.DecimalField(
        verbose_name="Цена iPhone",
        max_digits=15,
        decimal_places=2
    )
    processor = models.ForeignKey(
        ProcessorIphone,
        verbose_name="Процессор iPhone",
        max_length=50,
        on_delete=models.CASCADE
    )
    screen = models.ManyToManyField(
        ScreenIphone,
        verbose_name="Экран iPhone",
        related_name="iPhones",
    )

    class Meta:
        verbose_name = 'iPhone'
        verbose_name_plural = 'iPhones'

    def __str__(self):
        return f"{self.model} iPhone"


@receiver(pre_save, sender=Iphone)
def update_price_from_rom(sender, instance, **kwargs):
    instance.price = instance.rom.price


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

