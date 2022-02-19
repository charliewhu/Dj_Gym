# Generated by Django 3.2.8 on 2022-02-19 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20220215_2037'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingSplitDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('training_split', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.trainingsplit')),
            ],
        ),
    ]
