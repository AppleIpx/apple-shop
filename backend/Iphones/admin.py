from django.contrib import admin
from . import models


@admin.register(models.Color)
class ColorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('color',)}


admin.site.register(models.ProcessorIphone)
admin.site.register(models.ScreenIphone)


@admin.register(models.IphoneRom)
class IphoneRomAdmin(admin.ModelAdmin):
    list_filter = (
        'model',
    )


@admin.register(models.Iphone)
class IphoneAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'model',
        'image',
        'text',
    )


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'iphone'
    )
    list_editable = (
        'user',
        'iphone'
    )
    ordering = ("user",)


@admin.register(models.ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'iphone'
    )
    list_editable = (
        'user',
        'iphone'
    )
