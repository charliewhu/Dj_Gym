# Generated by Django 3.2.8 on 2022-06-10 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0044_auto_20220610_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='progression_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exercises.progressiontype'),
        ),
    ]
