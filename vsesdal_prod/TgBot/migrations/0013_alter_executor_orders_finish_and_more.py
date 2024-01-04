# Generated by Django 5.0 on 2024-01-02 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TgBot', '0012_alter_executor_orders_finish_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='executor',
            name='orders_finish',
            field=models.CharField(blank=True, default='', max_length=1000000000000, verbose_name='Законченные заказы'),
        ),
        migrations.AlterField(
            model_name='executor',
            name='orders_in_progress',
            field=models.CharField(blank=True, default='', max_length=1000000000000, verbose_name='Заказы в работе'),
        ),
        migrations.AlterField(
            model_name='executor',
            name='pay_history',
            field=models.CharField(blank=True, default='', max_length=10000000000000000000000000, verbose_name='История платежей'),
        ),
    ]
