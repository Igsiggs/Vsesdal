# Generated by Django 5.0 on 2023-12-24 00:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Parser', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accounts',
            options={'verbose_name': 'Аккаунт', 'verbose_name_plural': 'Аккаунты'},
        ),
        migrations.AlterModelOptions(
            name='categories',
            options={'verbose_name': 'Категорию', 'verbose_name_plural': 'Категории парсинга'},
        ),
    ]