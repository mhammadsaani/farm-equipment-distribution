# Generated by Django 4.0.6 on 2022-11-11 00:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_alter_questionfield_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questionfield',
            old_name='type',
            new_name='field_type',
        ),
    ]
