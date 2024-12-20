# Generated by Django 5.1.3 on 2024-11-30 01:29

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_remove_user_is_guest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playerprofile',
            name='daily_streak',
        ),
        migrations.RemoveField(
            model_name='playerprofile',
            name='is_guest',
        ),
        migrations.RemoveField(
            model_name='playerprofile',
            name='last_played',
        ),
        migrations.AlterField(
            model_name='friend',
            name='friendship_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Time of friendship creation'),
        ),
        migrations.AlterField(
            model_name='playerprofile',
            name='dob',
            field=models.DateField(default='1970-01-01', verbose_name='date of birth'),
        ),
        migrations.AlterField(
            model_name='playerprofile',
            name='join_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Account creation date'),
        ),
        migrations.AlterField(
            model_name='playerprofile',
            name='profile_picture',
            field=models.ImageField(default='default-profile-icon.png', upload_to='profile-pictures/', verbose_name='Profile picture'),
        ),
        migrations.AlterField(
            model_name='playerprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='playerprofile',
            name='username',
            field=models.CharField(default=uuid.UUID('ef620121-da75-4d35-8c99-31f92216a2c2'), max_length=60, unique=True, verbose_name='Username'),
        ),
    ]
