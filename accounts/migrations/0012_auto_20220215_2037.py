# Generated by Django 3.2.8 on 2022-02-15 20:37

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_userprofile_training_split'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birth_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.gender'),
        ),
        migrations.AddField(
            model_name='user',
            name='height',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='training_days',
            field=models.PositiveIntegerField(default=4, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(7)]),
        ),
        migrations.AddField(
            model_name='user',
            name='training_focus',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.trainingfocus'),
        ),
        migrations.AddField(
            model_name='user',
            name='training_split',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.trainingsplit'),
        ),
        migrations.AddField(
            model_name='user',
            name='weight',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
