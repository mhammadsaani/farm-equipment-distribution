# Generated by Django 4.0.6 on 2022-11-22 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_response_group_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='response',
            name='user',
        ),
    ]
