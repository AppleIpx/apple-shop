from django.contrib import admin
from . import models


@admin.register(models.IphoneColor)
class IphoneColorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('color',)}


admin.site.register(models.IphoneProcessor)
admin.site.register(models.IphoneDiagonal)
admin.site.register(models.IphoneMobileConnection)
admin.site.register(models.IphoneCountCamera)
admin.site.register(models.IphoneTypeOfScreen)
admin.site.register(models.IphoneModel)


@admin.register(models.IphoneRom)
class IphoneRomAdmin(admin.ModelAdmin):
    list_filter = (
        'rom',
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
        'iphone',
        'price_at_purchase',
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
        'iphone',
        'price_at_purchase'
    )
    list_editable = (
        'user',
        'iphone',
    )
