# Generated by Django 3.2.8 on 2022-02-15 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routines', '0042_rename_generate_sets_workoutexercise_is_set_generate'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='is_exercise_generate',
            field=models.BooleanField(default=0),
        ),
    ]
