# Generated by Django 5.1.3 on 2024-11-23 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_alter_item_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='is_daily',
            field=models.BooleanField(default=False, verbose_name='Daily item'),
        ),
        migrations.AddField(
            model_name='item',
            name='used_as_daily',
            field=models.BooleanField(default=False, verbose_name='Item used as daily'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of comment written'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(default='defaults/grocery-item.jpg', upload_to='item-images/', verbose_name='Item image'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.TextField(default='Kroger item', verbose_name='Item name'),
        ),
    ]
