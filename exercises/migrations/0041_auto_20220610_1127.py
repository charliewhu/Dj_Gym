# Generated by Django 3.2.8 on 2022-06-10 10:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0040_auto_20220609_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='max_rir',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AddField(
            model_name='exercise',
            name='min_rir',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='max_reps',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(30)]),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='min_reps',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(20)]),
        ),
    ]
