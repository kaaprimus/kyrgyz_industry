# Generated by Django 4.0.8 on 2022-12-04 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_rename_language_management_language_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='news',
            name='Short_Description',
            field=models.CharField(max_length=150, verbose_name='Краткое описание'),
        ),
    ]