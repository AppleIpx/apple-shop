from django.db import models


class ScreenIphone(models.Model):
    DIAGONAL_CHOICES = [
        ("diagonal_5_4", "5.4"),
        ("diagonal_5_8", "5.8"),
        ("diagonal_6_1", "6.1"),
        ("diagonal_6_5", "6.5"),
        ("diagonal_6_7", "6.7"),
    ]
    TYPE_CHOICES = [
        ("IPS", "Liquid Retina IPS LCD"),
        ("Retina_OLED", "Super Retina XDR OLED")
    ]
    RESOLUTION_CHOICES = [
        ("resolution_1792x828", "1792 x 828"),
        ("resolution_2340х1080", "2340 х 1080"),
        ("resolution_2436x1125", "2436 x 1125"),
        ("resolution_2532х1170", "2532 х 1170"),
        ("resolution_2556x1179", "2556 x 1179"),
        ("resolution_2688x1242", "2688 x 1242"),
        ("resolution_2778x1284", "2778 x 1284"),
        ("resolution_2796x1290", "2796 x 1290"),
    ]
    BRIGHTNESS_CHOICES = [
        ("brightness_625_nit", "До 625 нит"),
        ("brightness_1000_nit", "До 1000 нит"),
        ("brightness_1200_nit", "До 1200 нит"),
        ("brightness_1600_nit", "До 1600 нит"),
        ("brightness_2000_nit", "До 2000 нит"),
    ]
    CONTRAST_CHOICES = [
        ("сontrast_1400", "1400:1"),
        ("сontrast_2000000", "2000000:1"),
    ]
    PIXEL_PROCITY_CHOICES = [
        ("pixel_procity_326", "326 пикс/дюйм"),
        ("pixel_procity_458", "458 пикс/дюйм"),
        ("pixel_procity_460", "460 пикс/дюйм"),
    ]

    # DISPLAY_TECHNOLOGIES_CHOICES = [
    #     ("display_technologies_11", "True Tone"),
    # ]

    diagonal = models.CharField(verbose_name="Диагональ экрана", max_length=50, choices=DIAGONAL_CHOICES)
    type = models.CharField(verbose_name="Тип экрана", max_length=50, choices=TYPE_CHOICES)
    resolution = models.CharField(verbose_name="Разрешение", max_length=50, choices=RESOLUTION_CHOICES)
    brightness = models.CharField(verbose_name="Яркость", max_length=50, choices=BRIGHTNESS_CHOICES)
    contrast = models.CharField(verbose_name="Контрастность", max_length=50, choices=CONTRAST_CHOICES)
    pixel_procity = models.CharField(
        verbose_name="Плотность пикселей на дюйм", max_length=50, choices=PIXEL_PROCITY_CHOICES
    )
    # display_technologies =


class ProcessorIphone(models.Model):
    PROCESSOR_CHOICES = [
        ("A13", "A13 Bionic"),
        ("A14", "A14 Bionic"),
        ("A15", "A15 Bionic"),
        ("A16", "A16 Bionic"),
        ("A17", "A17 Bionic Pro"),
    ]
    processor = models.CharField(verbose_name="Процессор", max_length=20, choices=PROCESSOR_CHOICES)


class MobileConnectionIphone(models.Model):
    CONNECTION_CHOICES = [
        ("SIM_ESIM", "SIM/ESIM"),
        ("DUAL_SIM", "DUAL_SIM"),
        ("ESIM", "ESIM"),
    ]
    connection = models.CharField(verbose_name="Связь", max_length=20, choices=CONNECTION_CHOICES)


class RomIphone(models.Model):
    SIZE_CHOICES = [
        ("64", "64GB"),
        ("128", "128GB"),
        ("256", "256GB"),
        ("512", "512GB"),
        ("1024", "1024GB")
    ]

    size = models.CharField(
        verbose_name="Объем памяти",
        choices=SIZE_CHOICES,
        unique=True,
        max_length=10
    )


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
    # rom = models.ManyToManyField(
    #     RomIphone,
    #     verbose_name="Объем памяти",
    #     # through="iPhoneRom",
    #     related_name="iPhones",
    # )
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
    mobile_connection = models.ManyToManyField(
        MobileConnectionIphone,
        verbose_name="Связь",
        # through="iPhoneConnection",
        related_name="iPhones",
    )
    price = models.DecimalField(
        verbose_name="Цена iPhone",
        max_digits=10,
        decimal_places=2
    )
    processor = models.ManyToManyField(
        ProcessorIphone,
        verbose_name="Процессор iPhone",
        # through="iPhoneProcessor",
        related_name = "iPhones",
    )
    screen = models.ManyToManyField(
        ScreenIphone,
        verbose_name="Экран iPhone",
        # through="iPhoneScreen",
        related_name="iPhones",
    )

    class Meta:
        verbose_name = 'iPhone'
        verbose_name_plural = 'iPhones'

    def __str__(self):
        return self.model
