# Generated by Django 3.2.8 on 2022-02-22 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20220222_1442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainingsplitday',
            name='force',
        ),
    ]