# Generated by Django 5.1.3 on 2024-11-22 05:22

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_playerprofile_fastest_guess'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerprofile',
            name='bio',
            field=models.TextField(default='', verbose_name='Bio'),
        ),
        migrations.AlterField(
            model_name='playerprofile',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='Email address'),
        ),
        migrations.AlterField(
            model_name='playerprofile',
            name='fastest_guess',
            field=models.TimeField(blank=True, default=None, null=True, verbose_name='Time of fastest guess'),
        ),
        migrations.AlterField(
            model_name='playerprofile',
            name='join_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Account creation date'),
        ),
        migrations.AlterField(
            model_name='playerprofile',
            name='profile_picture',
            field=models.ImageField(default='default-profile-icon.png', upload_to='', verbose_name='Profile picture'),
        ),
        migrations.AlterField(
            model_name='playerprofile',
            name='username',
            field=models.CharField(default='anonymous_user', max_length=60, unique=True, verbose_name='Username'),
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friendship_created', models.DateTimeField(verbose_name='Time of friendship creation')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to='accounts.playerprofile', verbose_name='From user')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='accounts.playerprofile', verbose_name='To user')),
            ],
        ),
    ]
