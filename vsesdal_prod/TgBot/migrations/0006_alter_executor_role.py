# Generated by Django 5.0 on 2023-12-31 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TgBot', '0005_alter_executor_orders_in_progress_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='executor',
            name='role',
            field=models.CharField(choices=[('Админ', 'admin'), ('Исполнитель', 'executor')], default='Исполнитель', max_length=11, verbose_name='Роль'),
        ),
    ]