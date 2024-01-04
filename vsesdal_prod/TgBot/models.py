from django.db import models


class Executor(models.Model):
    class Meta:
        verbose_name = 'Исполнителя'
        verbose_name_plural = 'Исполнители'

    external_id = models.PositiveIntegerField(
        verbose_name='ID Исполнителя',
    )

    tg_name = models.TextField(
        verbose_name='Телеграм аккаунт',
        max_length=32,
    )

    role = models.CharField(
        max_length=13,
        verbose_name='Роль',
        choices=[
            ('Администратор', 'Администратор'),
            ('Исполнитель', 'Исполнитель'),
        ],
        default='Исполнитель',
    )

    balance = models.IntegerField(
        verbose_name='Баланс',
        default=0,
    )

    orders_finish = models.CharField(
        verbose_name='Законченные заказы',
        max_length=1000000000000,
        blank=True,
        default='',
    )

    orders_in_progress = models.CharField(
        verbose_name='Заказы в работе',
        max_length=1000000000000,
        blank=True,
        default='',
    )
    pay_history = models.CharField(
        verbose_name='История платежей',
        max_length=10000000000000000000000000,
        blank=True,
        default='',
    )


class OptionsTgBot(models.Model):
    class Meta:
        verbose_name = 'параметры'
        verbose_name_plural = 'Настройки TgBot'

    options = models.TextField(
        verbose_name='Параметр',
        max_length=1024,
    )
    values = models.CharField(
        verbose_name='Значение',
        max_length=2048,
    )

