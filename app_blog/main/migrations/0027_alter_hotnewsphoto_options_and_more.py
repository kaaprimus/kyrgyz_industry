# Generated by Django 4.0.8 on 2022-11-29 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_management_language_alter_hotnews_short_description_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hotnewsphoto',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='hotnews',
            name='short_description',
            field=models.CharField(max_length=130, verbose_name='Краткое описание'),
        ),
        migrations.AlterField(
            model_name='hotnews',
            name='title',
            field=models.CharField(max_length=70, verbose_name='Название событии'),
        ),
    ]