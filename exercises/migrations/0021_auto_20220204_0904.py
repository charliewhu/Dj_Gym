# Generated by Django 3.2.8 on 2022-02-04 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0020_remove_progressiontype_force'),
    ]

    operations = [
        migrations.RenameField(
            model_name='progressiontype',
            old_name='max_rir',
            new_name='target_rir',
        ),
        migrations.RemoveField(
            model_name='progressiontype',
            name='min_rir',
        ),
    ]
