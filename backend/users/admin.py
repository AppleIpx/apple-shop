from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    fields = (
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'password'
    )
    search_fields = (
        'username',
        'email'
    )