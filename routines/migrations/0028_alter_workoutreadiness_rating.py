# Generated by Django 3.2.8 on 2021-11-01 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routines', '0027_alter_workout_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutreadiness',
            name='rating',
            field=models.IntegerField(choices=[(1, 'Poorest'), (2, 'Poorer'), (3, 'Medium'), (4, 'Better'), (5, 'Best')]),
        ),
    ]