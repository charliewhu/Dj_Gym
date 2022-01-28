# Generated by Django 3.2.8 on 2022-01-28 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0009_auto_20220127_1356'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rir',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rir', models.PositiveIntegerField()),
                ('reps', models.PositiveIntegerField()),
                ('percent', models.FloatField()),
            ],
        ),
    ]
