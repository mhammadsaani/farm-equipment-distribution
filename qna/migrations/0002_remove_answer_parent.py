# Generated by Django 4.0.6 on 2022-08-09 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qna', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='parent',
        ),
    ]