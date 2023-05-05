# Generated by Django 4.1.6 on 2023-05-03 17:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_category_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='available',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
