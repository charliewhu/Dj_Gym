# Generated by Django 3.2.8 on 2022-02-24 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_rename_trainingsplit_split'),
    ]

    operations = [
        migrations.RenameField(
            model_name='frequencyallocation',
            old_name='training_split',
            new_name='split',
        ),
        migrations.RenameField(
            model_name='trainingsplititem',
            old_name='training_split',
            new_name='split',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='training_split',
            new_name='split',
        ),
    ]
