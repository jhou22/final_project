# Generated by Django 5.1.3 on 2024-11-25 20:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_guestprofile_dob'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guestprofile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='guestprofile',
            name='username',
        ),
    ]