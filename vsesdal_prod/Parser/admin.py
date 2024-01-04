from django.contrib import admin
from .models import Accounts, Categories


class CategoriesAdmin(admin.ModelAdmin):
    list_display = [
        'price',
        'categories',
    ]


class AccountsAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'email',
        'password',
        'proxy_address',
        'proxy_login',
    ]


admin.site.register(
    Accounts,
    AccountsAdmin,
)

admin.site.register(
    Categories,
    CategoriesAdmin,
)
