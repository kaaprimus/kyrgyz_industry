# Generated by Django 4.1.3 on 2022-12-12 17:05

import django.core.validators
from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_reports'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reports',
            name='url',
            field=models.FileField(upload_to=main.models.get_file_path, validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc'])], verbose_name='Путь файла'),
        ),
    ]
