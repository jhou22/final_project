# Generated by Django 5.1.3 on 2024-11-22 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(null=True, upload_to='item-images/', verbose_name='Item image'),
        ),
    ]
