# Generated by Django 3.1.2 on 2020-11-08 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_auto_20201107_1132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='stock',
        ),
    ]
