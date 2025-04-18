# Generated by Django 5.2 on 2025-04-17 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0006_log_forgotten_alter_log_size_alter_log_weight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='last_used_date',
        ),
        migrations.RemoveField(
            model_name='log',
            name='usage_date',
        ),
        migrations.RemoveField(
            model_name='log',
            name='usage_time',
        ),
        migrations.AddField(
            model_name='log',
            name='forgotten_item_place',
            field=models.BooleanField(null=True),
        ),
    ]
