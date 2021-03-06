# Generated by Django 3.2.8 on 2022-02-01 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0015_alter_purpose_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progressiontype',
            name='purpose',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exercises.purpose'),
        ),
        migrations.AlterField(
            model_name='purpose',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
