# Generated by Django 3.2.8 on 2022-02-01 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0014_alter_purpose_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purpose',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]