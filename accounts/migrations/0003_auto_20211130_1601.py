# Generated by Django 3.2.8 on 2021-11-30 16:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0004_alter_exercise_tier'),
        ('accounts', '0002_gender_profile_trainingfocus'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMetrics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.PositiveSmallIntegerField(null=True)),
                ('weight', models.PositiveSmallIntegerField(null=True)),
                ('birth_date', models.DateField(null=True)),
                ('training_days', models.PositiveIntegerField(default=4, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(7)])),
                ('gender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.gender')),
            ],
        ),
        migrations.CreateModel(
            name='UserRM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('one_rep_max', models.PositiveIntegerField()),
                ('date', models.DateField(auto_now=True)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercises.exercise')),
            ],
        ),
        migrations.RemoveField(
            model_name='usergroup',
            name='users',
        ),
        migrations.RemoveField(
            model_name='user',
            name='profile_pic',
        ),
        migrations.RenameModel(
            old_name='TrainingFocus',
            new_name='TrainingPhase',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.DeleteModel(
            name='UserGroup',
        ),
        migrations.AddField(
            model_name='userrm',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='training_focus',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.trainingphase'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
