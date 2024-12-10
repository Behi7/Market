# Generated by Django 5.1.3 on 2024-12-06 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Goods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=' ', max_length=200, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=' ', max_length=200, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subcategory',
            name='slug',
            field=models.SlugField(default=' ', max_length=200, unique=True),
            preserve_default=False,
        ),
    ]
