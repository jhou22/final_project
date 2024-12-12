# Generated by Django 5.1.3 on 2024-12-11 20:27

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_alter_playerprofile_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerprofile',
            name='bio',
            field=models.TextField(default='No information written.', verbose_name='Bio'),
        ),
        migrations.AlterField(
            model_name='playerprofile',
            name='dob',
            field=models.DateField(default='1970-01-01', verbose_name='Date of birth'),
        ),
        migrations.AlterField(
            model_name='playerprofile',
            name='profile_picture',
            field=models.ImageField(default='defaults/profile-icon.png', upload_to='profile-pictures/', verbose_name='Profile picture'),
        ),
        migrations.AlterField(
            model_name='playerprofile',
            name='username',
            field=models.CharField(default=uuid.UUID('819d6fb7-651c-4253-97ef-308ea3143d3e'), max_length=60, unique=True, verbose_name='Username'),
        ),
    ]