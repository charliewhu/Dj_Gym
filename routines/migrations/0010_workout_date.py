# Generated by Django 3.2.8 on 2021-10-13 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routines', '0009_remove_workoutitem_muscle_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
