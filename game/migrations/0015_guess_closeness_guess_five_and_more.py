# Generated by Django 5.1.3 on 2024-12-09 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0014_guess_correctly_guessed'),
    ]

    operations = [
        migrations.AddField(
            model_name='guess',
            name='closeness_guess_five',
            field=models.CharField(blank=True, default=None, max_length=20, null=True, verbose_name='Guess 5 closeness'),
        ),
        migrations.AddField(
            model_name='guess',
            name='closeness_guess_four',
            field=models.CharField(blank=True, default=None, max_length=20, null=True, verbose_name='Guess 4 closeness'),
        ),
        migrations.AddField(
            model_name='guess',
            name='closeness_guess_one',
            field=models.CharField(blank=True, default=None, max_length=20, null=True, verbose_name='Guess 1 closeness'),
        ),
        migrations.AddField(
            model_name='guess',
            name='closeness_guess_six',
            field=models.CharField(blank=True, default=None, max_length=20, null=True, verbose_name='Guess 6 closeness'),
        ),
        migrations.AddField(
            model_name='guess',
            name='closeness_guess_three',
            field=models.CharField(blank=True, default=None, max_length=20, null=True, verbose_name='Guess 3 closeness'),
        ),
        migrations.AddField(
            model_name='guess',
            name='closeness_guess_two',
            field=models.CharField(blank=True, default=None, max_length=20, null=True, verbose_name='Guess 2 closeness'),
        ),
    ]
