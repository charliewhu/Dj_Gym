# Generated by Django 3.2.8 on 2022-01-27 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0007_alter_exercise_tier'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseVolume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
