# Generated by Django 5.1.3 on 2024-12-10 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0017_alter_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemimage',
            name='image_file',
            field=models.ImageField(blank=True, null=True, upload_to='item-images/'),
        ),
    ]