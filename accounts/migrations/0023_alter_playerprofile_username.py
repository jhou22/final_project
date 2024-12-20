# Generated by Django 5.1.3 on 2024-12-10 22:33

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_alter_playerprofile_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerprofile',
            name='username',
            field=models.CharField(default=uuid.UUID('39d145cc-ac26-483c-8f2a-ca31a4cc4638'), max_length=60, unique=True, verbose_name='Username'),
        ),
    ]
