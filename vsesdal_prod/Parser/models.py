from django.db import models


class Accounts(models.Model):
    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

    external_id = models.PositiveIntegerField(
        verbose_name='ID Аккаунта',
    )

    password = models.TextField(
        verbose_name='Пароль от аккаунта',
        max_length=100,
    )

    email = models.EmailField(
        verbose_name='Почта от аккаунта',
    )

    proxy_address = models.TextField(
        verbose_name='Адрес proxy',
        max_length=32,
    )

    proxy_login = models.TextField(
        verbose_name='Логин proxy',
        max_length=16,
    )


class Categories(models.Model):
    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории парсинга'

    price = models.IntegerField(
        verbose_name='Цена',
    )

    categories = models.TextField(
        verbose_name='Категория',
        max_length=32,
    )


