# Generated by Django 5.1.3 on 2024-11-24 21:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_guestprofile_playerprofile_daily_streak_and_more'),
        ('game', '0003_item_is_daily_item_used_as_daily_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='item',
        ),
        migrations.RemoveField(
            model_name='item',
            name='is_daily',
        ),
        migrations.AlterField(
            model_name='comment',
            name='message',
            field=models.TextField(verbose_name='Message'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.playerprofile', verbose_name='User'),
        ),
        migrations.CreateModel(
            name='DailyPuzzle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Date of daily puzzle')),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='game.item', verbose_name='Item')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='puzzle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='game.dailypuzzle', verbose_name='Daily Puzzle'),
        ),
        migrations.CreateModel(
            name='PracticePuzzle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='game.item', verbose_name='Item')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Guess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_profile_type', models.CharField(choices=[('P', 'PlayerProfile'), ('G', 'GuestProfile')], default='P', max_length=1)),
                ('owner_puzzle_type', models.CharField(choices=[('D', 'DailyPuzzle'), ('P', 'PracticePuzzle')], default='P', max_length=1)),
                ('guess_one', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Guess 1')),
                ('guess_two', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Guess 2')),
                ('guess_three', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Guess 3')),
                ('guess_four', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Guess 4')),
                ('guess_five', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Guess 5')),
                ('guess_six', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Guess 6')),
                ('owner_daily_puzzle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.dailypuzzle', verbose_name='Daily puzzle')),
                ('owner_guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.guestprofile', verbose_name='Guest profile')),
                ('owner_player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.playerprofile', verbose_name='Player profile')),
                ('owner_practice_puzzle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.practicepuzzle', verbose_name='Practice puzzle')),
            ],
            options={
                'constraints': [models.CheckConstraint(condition=models.Q(models.Q(('owner_guest_id__isnull', True), ('owner_profile_type', 'G')), models.Q(('owner_player_id__isnull', True), ('owner_profile_type', 'P')), _connector='OR'), name='game_guess_profile_type_only_one_owner'), models.CheckConstraint(condition=models.Q(models.Q(('owner_daily_puzzle_id__isnull', True), ('owner_puzzle_type', 'D')), models.Q(('owner_practice_puzzle_id__isnull', True), ('owner_puzzle_type', 'P')), _connector='OR'), name='game_guess_puzzle_type_only_one_owner')],
            },
        ),
    ]