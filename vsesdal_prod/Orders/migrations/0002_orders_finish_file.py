# Generated by Django 5.0 on 2024-01-03 16:12

import Orders.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='finish_file',
            field=models.FileField(default='', upload_to=Orders.models.image_path, verbose_name='Законченные файлы'),
        ),
    ]
