from datetime import date
from django.db import models


def finish_path(instance, filename):
    return '/'.join(['finish/', str(instance.id_order), filename])


def image_path(instance, filename):
    return '/'.join(['orders/', str(instance.id_order), filename])


class Orders(models.Model):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    id_order = models.IntegerField(
        verbose_name='id заказа',
        default=0,
    )

    title = models.CharField(
        verbose_name='Название заказа',
        max_length=128,
    )

    price = models.IntegerField(
        verbose_name='Цена',
        default=0,
    )

    text = models.TextField(
        verbose_name='Описание заказа',
        max_length=1024,
    )

    files = models.FileField(
        verbose_name='Файлы заказа',
        upload_to=image_path,
    )

    deadline = models.DateField(
        verbose_name='Срок исполнения',
    )

    antiplug = models.TextField(
        verbose_name='Антиплагиат',
        max_length=32,
    )

    categories = models.TextField(
        verbose_name='Категория',
        max_length=64,
    )

    status = models.TextField(
        verbose_name='Статус заказа',
        max_length=32,
    )

    date = models.DateTimeField(
        verbose_name='Время добавления',
        auto_now_add=True,
    )

    finish_file = models.FileField(
        verbose_name='Законченные файлы',
        upload_to=finish_path,
        default='',
        blank=True,
    )