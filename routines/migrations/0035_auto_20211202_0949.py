# Generated by Django 3.2.8 on 2021-12-02 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('routines', '0034_auto_20211130_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutexercise',
            name='workout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='routines.workout'),
        ),
        migrations.AlterField(
            model_name='workoutexerciseset',
            name='workout_exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sets', to='routines.workoutexercise'),
        ),
    ]
