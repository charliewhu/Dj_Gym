# Generated by Django 3.2.8 on 2022-02-22 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0033_remove_force_training_day'),
        ('accounts', '0018_remove_trainingsplitday_force'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingsplitday',
            name='force',
            field=models.ManyToManyField(through='accounts.TrainingSplitDayForce', to='exercises.Force'),
        ),
    ]
