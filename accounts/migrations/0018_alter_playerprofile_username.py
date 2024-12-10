# Generated by Django 5.1.3 on 2024-12-09 21:18

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_alter_playerprofile_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerprofile',
            name='username',
            field=models.CharField(default=uuid.UUID('9a8bd5f5-7448-453c-8bd4-5c8d59463dab'), max_length=60, unique=True, verbose_name='Username'),
        ),
    ]