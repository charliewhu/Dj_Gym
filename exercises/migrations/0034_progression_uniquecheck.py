# Generated by Django 3.2.8 on 2022-02-23 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0033_remove_force_training_day'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='progression',
            constraint=models.UniqueConstraint(fields=('progression_type', 'rep_delta', 'rir_delta'), name='UniqueCheck'),
        ),
    ]
