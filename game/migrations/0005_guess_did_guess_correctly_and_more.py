# Generated by Django 5.1.3 on 2024-11-24 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_remove_comment_item_remove_item_is_daily_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='guess',
            name='did_guess_correctly',
            field=models.BooleanField(default=False, verbose_name='Did guess item price correctly'),
        ),
        migrations.AddField(
            model_name='guess',
            name='number_of_guesses_left',
            field=models.IntegerField(default=6, verbose_name='Number of guesses left'),
        ),
    ]