# Generated by Django 5.2 on 2025-04-17 05:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0002_remove_log_usage_place'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='name',
        ),
    ]
