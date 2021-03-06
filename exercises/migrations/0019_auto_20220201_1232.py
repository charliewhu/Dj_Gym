# Generated by Django 3.2.8 on 2022-02-01 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0018_auto_20220201_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='progressiontype',
            name='max_reps',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='progressiontype',
            name='max_rir',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='progressiontype',
            name='min_reps',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='progressiontype',
            name='min_rir',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
