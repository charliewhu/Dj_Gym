# Generated by Django 3.2.8 on 2022-02-01 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_rename_trainingphase_trainingfocus'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserRM',
        ),
    ]
