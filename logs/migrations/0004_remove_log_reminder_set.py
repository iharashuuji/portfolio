# Generated by Django 5.2 on 2025-04-17 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0003_remove_log_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='reminder_set',
        ),
    ]
