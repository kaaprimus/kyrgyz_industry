# Generated by Django 4.1.3 on 2022-12-12 16:54

import django.core.validators
from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_alter_projects_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='Название отчета')),
                ('short_description', models.CharField(max_length=130, verbose_name='Краткое описание')),
                ('url', models.FileField(upload_to=main.models.get_file_path, validators=[django.core.validators.validate_image_file_extension], verbose_name='Путь файла')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
