# Generated by Django 3.2.8 on 2021-12-02 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0004_alter_exercise_tier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='tier',
            field=models.CharField(choices=[(1, 'T1'), (2, 'T2'), (3, 'T3'), (4, 'Other'), (5, 'Best')], help_text='T1 exercises are the competition exercises.            T2 exercises are close variations of the main lifts.             T3 exercises develop the musculature eg. quads for squats.             Other exercises develop supplementary muscles', max_length=60),
        ),
    ]