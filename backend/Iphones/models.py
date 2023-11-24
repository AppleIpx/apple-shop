from django.db import models


class ScreenIphone(models.Model):
    model = models.CharField(
        verbose_name="Экран для iPhone",
        max_length=50
        # on_delete=models.CASCADE
    )
    diagonal = models.CharField(
        verbose_name="Диагональ",
        max_length=100,
        unique=True,
    )
    type_of_screen = models.CharField(
        verbose_name="Тип",
        max_length=100,
        unique=True,
    )
    resolution = models.CharField(
        verbose_name="Разрешение",
        max_length=50,
        unique=True,
    )
    brightness = models.CharField(
        verbose_name="Яркость",
        max_length=50,
        unique=True,
    )

    CONTRAST_CHOICES = [
        ("сontrast_1400", "1400:1"),
        ("сontrast_2000000", "2000000:1"),
    ]
    pixel_procity = models.CharField(
        verbose_name="пикс/дюйм",
        max_length=50,
        unique=True,
    )

    contrast = models.CharField(verbose_name="Контрастность", max_length=50, choices=CONTRAST_CHOICES)

    def __str__(self):
        return self.model


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
        related_name="iPhones",
        on_delete=models.CASCADE
    )
    SIZE_CHOICES = [
        ("64", "64GB"),
        ("128", "128GB"),
        ("256", "256GB"),
        ("512", "512GB"),
        ("1024", "1024GB")
    ]

    rom = models.CharField(
        verbose_name="Объем памяти",
        choices=SIZE_CHOICES,
        unique=True,
        max_length=10
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
        return self.model
