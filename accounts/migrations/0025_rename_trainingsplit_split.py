# Generated by Django 3.2.8 on 2022-02-24 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_alter_trainingsplitday_training_split_item'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TrainingSplit',
            new_name='Split',
        ),
    ]
