# Generated by Django 3.2.8 on 2021-10-12 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routines', '0002_auto_20211012_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='name',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]
