# Generated by Django 5.1.3 on 2024-11-30 01:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_remove_playerprofile_daily_streak_and_more'),
        ('game', '0011_rename_owner_player_guess_owner_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guess',
            name='did_guess_correctly',
        ),
        migrations.RemoveField(
            model_name='guess',
            name='number_of_guesses_left',
        ),
        migrations.RemoveField(
            model_name='guess',
            name='owner_daily_puzzle',
        ),
        migrations.RemoveField(
            model_name='guess',
            name='owner_practice_puzzle',
        ),
        migrations.RemoveField(
            model_name='guess',
            name='owner_puzzle_type',
        ),
        migrations.RemoveField(
            model_name='item',
            name='used_as_daily',
        ),
        migrations.AddField(
            model_name='guess',
            name='daily_puzzle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.dailypuzzle', verbose_name='Daily Puzzle'),
        ),
        migrations.AddField(
            model_name='guess',
            name='practice_puzzle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.practicepuzzle', verbose_name='Practice Puzzle'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='message',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='comment',
            name='puzzle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.dailypuzzle', verbose_name='Puzzle where comment is written'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.playerprofile'),
        ),
        migrations.AlterField(
            model_name='dailypuzzle',
            name='item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='game.item', verbose_name='Puzzle item'),
        ),
        migrations.AlterField(
            model_name='guess',
            name='guess_five',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True, verbose_name='Guess 5'),
        ),
        migrations.AlterField(
            model_name='guess',
            name='guess_four',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True, verbose_name='Guess 4'),
        ),
        migrations.AlterField(
            model_name='guess',
            name='guess_one',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True, verbose_name='Guess 1'),
        ),
        migrations.AlterField(
            model_name='guess',
            name='guess_six',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True, verbose_name='Guess 6'),
        ),
        migrations.AlterField(
            model_name='guess',
            name='guess_three',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True, verbose_name='Guess 3'),
        ),
        migrations.AlterField(
            model_name='guess',
            name='guess_two',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True, verbose_name='Guess 2'),
        ),
        migrations.AlterField(
            model_name='guess',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.playerprofile', verbose_name='Owner of guess'),
        ),
        migrations.AlterField(
            model_name='practicepuzzle',
            name='item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='game.item', verbose_name='Puzzle item'),
        ),
    ]
