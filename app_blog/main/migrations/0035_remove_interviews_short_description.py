# Generated by Django 4.1.3 on 2022-12-15 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0034_alter_reports_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interviews',
            name='short_description',
        ),
    ]